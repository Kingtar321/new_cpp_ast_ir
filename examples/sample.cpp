#include <iostream>

namespace demo {
    class Base {
    public:
        virtual void greet();
    protected:
        int base_value;
    };

    class Derived : public Base {
    public:
        Derived(int x) : base_value(x) {}
        void greet() override {
            std::cout << "Hello " << base_value << std::endl;
        }
    private:
        int base_value;
    };

    int add(int a, int b) {
        return a + b;
    }
}
