#include <stdio.h> 
#include <stdint.h>
#include <math.h>

uint32_t xor128(void) { 
	static uint32_t x = 123456789;
	static uint32_t y = 362436069;
	static uint32_t z = 521288629;
	static uint32_t w = 88675123; 
	uint32_t t;
 
	t = x ^ (x << 11);
	x = y; y = z; z = w;
	return w = (w ^ (w >> 19)) ^ (t ^ (t >> 8)); 
}

uint32_t xor128_2(uint32_t minimum, uint32_t maximum) {

	// printf("max: %u\r\n", maximum);
	
	static uint32_t x = 123456789;
	static uint32_t y = 362436069;
	static uint32_t z = 521288629;
	static uint32_t w = 88675123; 
	uint32_t t;
 
	t = x ^ (x << 11);
	x = y; y = z; z = w;
	w = (w ^ (w >> 19)) ^ (t ^ (t >> 8));
	return (minimum + w) % maximum;
}

double xor128_3() {

	static uint32_t x = 123456789;
	static uint32_t y = 362436069;
	static uint32_t z = 521288629;
	static uint32_t w = 88675123; 
	uint32_t t;
 
	t = x ^ (x << 11);
	x = y; y = z; z = w;
	w = (w ^ (w >> 19)) ^ (t ^ (t >> 8));

	return (double)((1.0 / 4294967296.0) * w);
}


int main() 
{
	// printf("max: %d", sizeof(uint32_t));

	int i;
	for(i=0;i<10;i++){
		printf("%010u\r\n",xor128());
	}

	printf("-----\r\n");
	for(i=0;i<10;i++){
		printf("%010u\r\n",xor128_2(10, 1024));
	}

	printf("-----\r\n");
	for(i=0;i<10;i++){
		printf("%010u\r\n",xor128_2(4294967290, 4294967295));
	}

	printf("-----\r\n");
	uint32_t value = 2;
	printf("%010u\r\n",uint32_t(pow((double)value, 32.0) - 1) + 1);

	printf("%10.f\r\n",pow((double)value, 32.0));

	// printf("%10.f\r\n", 1.0 / uint32_t(pow((double)value, 32.0)));
	// printf("%10.f\r\n", 1.0 / (0xffffffff + 1));
	// printf("%10.f\r\n", 4294967296.0);
	// printf("%10.f\r\n", (float)4294967296.0);
	double dval = 4294967296.1209;
	float fval = 429.1209f;
	printf("%f\r\n", dval);
	printf("%f\r\n", fval);

	printf("-----\r\n");

	for(i=0;i<10;i++){
		printf("%10.16f\r\n", xor128_3());
	}

	return 0;
}
