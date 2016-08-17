#include <iostream>

uint32_t variableTypeTest();
void doubleCheck();
void intCheck();


int main(int argc, char *argv[]){
	std::cout << "Hello c++" << std::endl;

	std::cout << "" << variableTypeTest() << std::endl;

	std::cout << "//++++++++++++++++++++++++++++++++//" << std::endl;
	doubleCheck();
	std::cout << "//++++++++++++++++++++++++++++++++//" << std::endl;
	intCheck();
	return 0;
}


uint32_t variableTypeTest(){
	std::cout << "sizeof(uint64_t)=" << sizeof(uint64_t) << "byte" << std::endl;
	std::cout << "sizeof(uint32_t)=" << sizeof(uint32_t) << "byte" << std::endl;

	static uint64_t x = 88172645463325252ULL;
	std::cout << "x1 " << x << std::endl;
	x = x ^ (x << 13);
	std::cout << "x2 " << x << std::endl;
	x = x ^ (x >> 7);
	std::cout << "x3 " << x << std::endl;
	x = x ^ (x << 17);
	std::cout << "x4 " << x << std::endl;
	return x;
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
	// int a = 1103527590;
	std::cout << a << std::endl;

	for(int i=0; i<9; ++i){
		unsigned int b = a * 1103515245 + 12345;
		// int b = a * 1103515245 + 12345;
		std::cout << b << std::endl;
		a = b;
	}

	//unsigned int型でやってるので32ビットを超えたから勝手に捨てられる
	//pythonやrubyのように自分で2の32乗の剰余を取って32ビットに収めなくてよい
	// unsigned int c = b % 4294967296;
	// std::cout << c << std::endl;
}
