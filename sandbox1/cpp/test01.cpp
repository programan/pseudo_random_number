#include <iostream>

void doubleCheck();
void intCheck();

int main(int argc, char *argv[]){
	std::cout << "Hello c++" << std::endl;

	std::cout << "//++++++++++++++++++++++++++++++++//" << std::endl;
	doubleCheck();
	std::cout << "//++++++++++++++++++++++++++++++++//" << std::endl;
	intCheck();
	return 0;
}


void doubleCheck(){
	std::cout << "sizeof(double)=" << sizeof(double) << "byte" << std::endl;
	// std::cout << "double min = " << -DBL_MAX << endl;
	std::cout << "double min " << std::numeric_limits<double>::min() << std::endl;
	std::cout << "double max " << std::numeric_limits<double>::max() << std::endl;

	double d = 9007199254740992;
	std::cout << "9007199254740992" << std::endl;
	// std::cout << std::fixed;
	std::cout << d << std::endl;
	// std::cout << std::fixed << d << std::endl;
	// std::cout << std::showpoint << d << std::endl;

	std::cout << "----------------------" << std::endl;

	double a = 1103527590.0;
	std::cout << a << std::endl;
	
	double b = a * 1103515245 + 12345;
	std::cout << b << std::endl;

	std::cout << std::fixed;
	std::cout << b << std::endl;

	// double c = static_cast<double>(static_cast<int>(b) % 4294967296);
	double c = static_cast<int>(b) % 4294967296;
	std::cout << c << std::endl;
}


void intCheck(){
	std::cout << "sizeof(int)=" << sizeof(int) << "byte" << std::endl;

	unsigned int a = 1103527590;
	std::cout << a << std::endl;
	
	unsigned int b = a * 1103515245 + 12345;
	std::cout << b << std::endl;

	unsigned int c = b % 4294967296;
	std::cout << c << std::endl;
}
