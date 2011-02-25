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

void main(void)
{
	FILE *fp;
	char temp[1024];
	int bsize;

	fp = fopen("1.mpg", "rb");
	if (fp == NULL) {
		printf("can not open file\n");
		exit(0);
	}
	temp[1023] = '\0';

	while (!feof(fp)) {
		bsize = fread(temp, sizeof(unsigned char), sizeof(temp), fp);
		printf("%d字节被读取", bsize);
	}

	fclose(fp);

}
