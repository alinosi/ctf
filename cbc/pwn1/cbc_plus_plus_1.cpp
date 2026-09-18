

#include<iostream>
#include<vector>
#include<string>

std::string name;
std::vector<unsigned long long> *vec;

void init() {
    std::cout << "Your name: ";
    std::cin >> name;
    vec = new std::vector<unsigned long long>();
    vec->reserve(0x100);
}

void menu() {
    std::cout << "Hi, " << name << std::endl;
    std::cout << "1. Add new number" << std::endl;
    std::cout << "2. Swap numbers" << std::endl;
    std::cout << "3. Exit" << std::endl;
    std::cout << "> ";
}

int main() {

    init();

    int choice = 0, ind1 = 0, ind2 = 0;
    unsigned long long num = 0;

    while(1) {
        menu();
        std::cin >> choice;
        switch(choice)  {
            case 1:
                std::cout << "Num: ";
                std::cin >> num;
                vec->push_back(num);
                std::cout << "Done" << std::endl;
                break;
            case 2:
                std::cout << "Index 1: ";
                std::cin >> ind1;
                std::cout << "Index 2: ";
                std::cin >> ind2;
                num = vec->operator[](ind1);
                vec->operator[](ind1) = vec->operator[](ind2);
                vec->operator[](ind2) = num;
                std::cout << "Done" << std::endl;
                break;
            case 3:
                goto done;
            default:
                std::cout << "Invalid" << std::endl;
                break;
        }

    }
done:
    std::cout << "Bye!" << std::endl;
    return 0;
}
