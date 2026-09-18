FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app

RUN adduser -D ctf

COPY --from=builder /app ./

RUN apk add --no-cache gcc musl-dev

RUN mv flag.txt /root/flag.txt \
    && mv readflag.c /tmp/readflag.c \
    && gcc -o /readflag /tmp/readflag.c \
    && chown root:root /readflag \
    && chmod 4555 /readflag \
    && rm /tmp/readflag.c \
    && apk del gcc musl-dev

EXPOSE 3000

ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

USER ctf

CMD ["npm", "start"]