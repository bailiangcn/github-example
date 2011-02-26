/*
 * =====================================================================================
 *
 *       Filename:  checkmedia.c
 *
 *    Description:  打开一个媒体文件,输出媒体的属性
 *
 *        Version:  1.0
 *        Created:  2011年02月25日 18时50分00秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  bailiangcn@gmail.com
 * =====================================================================================
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFFERLEN 1024
#define SYNTIMES 3

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  check188or204
 *  Description:  判断一个数组是否是188或者204格式
 *                bsize 数组的长度
 *                temp  数组的实际数据指针
 *				  返回一个数组res
 *				  res[0] = 0 文件未检测到同步
 *				  res[0] = 188 检测到188同步,起始位置 res[1]
 *				  res[0] = 204 检测到204同步,起始位置 res[1]
 * =====================================================================================
 */
void check188or204(int bsize, unsigned char *temp, int *res)
{
	int fisrtsynpos = 0;
	int checkok = 0;

	for (int i = 0; i < bsize; i++) {
		if (temp[i] == 0x47) {
			for (int j = 1; j <= SYNTIMES; j++) {
				if (temp[i + 188 * j] != 0x47) {
					checkok = 1;
				}
			}
			if (checkok == 0) {
				res[0] = 188;
				res[1] = i;
				return;
			}
			for (int j = 1; j <= SYNTIMES; j++) {
				if (temp[i + 204 * j] != 0x47) {
					checkok = 1;
				}
			}
			if (checkok == 0) {
				res[0] = 204;
				res[1] = i;
				return;
			}
		}
	}

	res[0] = 0;
	return;
}

void printts(int bsize, unsigned char *data)
{
	for (int i = 0; i < bsize; i++) {
		printf("%x ", data[i]);
	}
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  main
 *  Description:  主调用程序
 * =====================================================================================
 */
int main(int argc, char *argv[])
{
	FILE *fp;
	unsigned char *p, temp[BUFFERLEN] = { 0 };
	int offset_packet, bsize = 0;
	char filename[256] = "1.ts";
	int syn[2] = { 0 };

	if (argc == 2) {
		strcpy(filename, argv[1]);
	}
	fp = fopen(filename, "rb");
	if (fp == NULL) {
		printf("文件打开失败,可能文件不存在\n");
		return -1;
	}

	bsize = fread(temp, sizeof(unsigned char), sizeof(temp), fp);
	printf("%s的%d字节被读取\n", filename, bsize);

	if (bsize > 188) {
		check188or204(bsize, temp, syn);
		switch (syn[0]) {
		case 0:
			printf("未找到同步\n");
			break;
		case 188:
		case 204:
			printf("找到%d同步符号,起始位置:%d \n",
			       syn[0], syn[1]);
			offset_packet = 0;
			p = &temp[syn[1] + syn[0] * offset_packet];
			printts(syn[0], p);

			break;
		}
	}

	fclose(fp);
	return 0;
}
