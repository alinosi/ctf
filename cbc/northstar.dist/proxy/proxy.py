import json
import os
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib import error, parse, request


MAX_PARAMS = 10
MAX_VALUE_LENGTH = 100
BLOCKED_TERM = "proto"
UPSTREAM_BASE = os.environ.get("UPSTREAM_BASE", "http://app:3000")
PROXY_HOST = os.environ.get("PROXY_HOST", "0.0.0.0")
PROXY_PORT = int(os.environ.get("PROXY_PORT", "8080"))
HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


def append_forwarded_for(existing_value: str | None, client_ip: str) -> str:
    if not existing_value:
        return client_ip

    return f"{existing_value}, {client_ip}"


def split_host_port(host_header: str):
    if not host_header:
        return "", None

    if host_header.startswith("["):
        closing_bracket = host_header.find("]")
        if closing_bracket == -1:
            return host_header, None

        host = host_header[: closing_bracket + 1]
        remainder = host_header[closing_bracket + 1 :]
        if remainder.startswith(":") and remainder[1:].isdigit():
            return host, remainder[1:]
        return host, None

    host, separator, port = host_header.rpartition(":")
    if separator and port.isdigit():
        return host, port

    return host_header, None


def build_forwarded_headers(headers, client_ip: str):
    forwarded_host = headers.get("Host", "")
    forwarded_proto = headers.get("X-Forwarded-Proto", "http")
    _, forwarded_port = split_host_port(forwarded_host)

    if not forwarded_port:
        forwarded_port = "443" if forwarded_proto == "https" else "80"

    return {
        "X-Forwarded-For": append_forwarded_for(
            headers.get("X-Forwarded-For"), client_ip
        ),
        "X-Forwarded-Host": forwarded_host,
        "X-Forwarded-Port": forwarded_port,
        "X-Forwarded-Proto": forwarded_proto,
    }


def flatten_json(prefix: str, value):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            nested_prefix = f"{prefix}.{key}" if prefix else str(key)
            yield from flatten_json(nested_prefix, nested_value)
        return

    if isinstance(value, list):
        for index, nested_value in enumerate(value):
            nested_prefix = f"{prefix}[{index}]"
            yield from flatten_json(nested_prefix, nested_value)
        return

    yield prefix, "" if value is None else str(value)


def parse_multipart_form_data(content_type: str, body: bytes):
    message_bytes = (
        f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8")
        + body
    )
    message = BytesParser(policy=policy.default).parsebytes(message_bytes)

    if not message.is_multipart():
        raise ValueError("Invalid multipart payload.")

    parameters = []

    for part in message.iter_parts():
        if part.get_content_disposition() != "form-data":
            continue

        field_name = part.get_param("name", header="content-disposition")
        if not field_name:
            continue

        filename = part.get_filename()
        if filename is not None:
            parameters.append((f"{field_name}.filename", filename))

        payload = part.get_payload(decode=True) or b""
        charset = part.get_content_charset() or "utf-8"

        try:
            value = payload.decode(charset, errors="replace")
        except LookupError:
            value = payload.decode("utf-8", errors="replace")

        parameters.append((field_name, value))

    return parameters


def collect_parameters(path: str, content_type: str, body: bytes):
    parameters = list(parse.parse_qsl(parse.urlsplit(path).query, keep_blank_values=True))

    if not body:
        return parameters, None

    media_type = content_type.split(";", 1)[0].strip().lower()

    if media_type == "application/x-www-form-urlencoded":
        body_text = body.decode("utf-8", errors="replace")
        parameters.extend(parse.parse_qsl(body_text, keep_blank_values=True))
        return parameters, None

    if media_type == "application/json":
        try:
            payload = json.loads(body.decode("utf-8", errors="replace"))
        except json.JSONDecodeError:
            return parameters, None

        if isinstance(payload, dict):
            parameters.extend(flatten_json("", payload))
        elif isinstance(payload, list):
            parameters.extend(flatten_json("body", payload))
        else:
            parameters.append(("body", str(payload)))

        return parameters, None

    if media_type == "multipart/form-data":
        try:
            parameters.extend(parse_multipart_form_data(content_type, body))
        except ValueError as exc:
            return parameters, (400, str(exc))

    return parameters, None


def validate_parameters(parameters):
    if len(parameters) > MAX_PARAMS:
        return 400, f"Too many parameters. Maximum allowed is {MAX_PARAMS}."

    blocked_term = BLOCKED_TERM.lower()

    for key, value in parameters:
        key_text = str(key)
        value_text = str(value)

        if len(key_text) > MAX_VALUE_LENGTH:
            return 400, f"Parameter name '{key_text}' exceeds {MAX_VALUE_LENGTH} characters."

        if len(value_text) > MAX_VALUE_LENGTH:
            return 400, f"Parameter '{key_text}' exceeds {MAX_VALUE_LENGTH} characters."

        if blocked_term in key_text.lower() or blocked_term in value_text.lower():
            return 403, "Request blocked by input policy."

    return None


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        self.handle_proxy()

    def do_POST(self):
        self.handle_proxy()

    def do_PUT(self):
        self.handle_proxy()

    def do_PATCH(self):
        self.handle_proxy()

    def do_DELETE(self):
        self.handle_proxy()

    def do_OPTIONS(self):
        self.handle_proxy()

    def handle_proxy(self):
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(content_length) if content_length > 0 else b""

        parameters, parse_error = collect_parameters(
            self.path, self.headers.get("Content-Type", ""), body
        )
        validation_error = parse_error or validate_parameters(parameters)
        if validation_error:
            status_code, message = validation_error
            self.respond_json(status_code, {"error": message})
            return

        upstream_url = f"{UPSTREAM_BASE}{self.path}"
        upstream_headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in HOP_BY_HOP_HEADERS
        }
        upstream_headers.update(
            build_forwarded_headers(self.headers, self.client_address[0])
        )

        upstream_request = request.Request(
            upstream_url,
            data=body if body else None,
            headers=upstream_headers,
            method=self.command,
        )

        try:
            with request.urlopen(upstream_request, timeout=15) as upstream_response:
                response_body = upstream_response.read()
                self.send_response(upstream_response.status)

                for header, value in upstream_response.headers.items():
                    if header.lower() in HOP_BY_HOP_HEADERS:
                        continue
                    self.send_header(header, value)

                self.send_header("Content-Length", str(len(response_body)))
                self.end_headers()
                self.wfile.write(response_body)
        except error.HTTPError as upstream_error:
            response_body = upstream_error.read()
            self.send_response(upstream_error.code)

            for header, value in upstream_error.headers.items():
                if header.lower() in HOP_BY_HOP_HEADERS:
                    continue
                self.send_header(header, value)

            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
        except error.URLError:
            self.respond_json(502, {"error": "Upstream service unavailable."})

    def respond_json(self, status_code: int, payload):
        response_body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer((PROXY_HOST, PROXY_PORT), ProxyHandler)
    print(f"Proxy listening on {PROXY_HOST}:{PROXY_PORT}, forwarding to {UPSTREAM_BASE}")
    server.serve_forever()
