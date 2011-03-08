/*
 * ==========================================================================
 *
 *       Filename:  tsb.c
 *
 *    Description:  播控程序的主调用程序
 *
 *        Version:  1.0
 *        Created:  2011年02月27日 11时50分57秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *        Company:  
 *
 * ==========================================================================
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "checkmedia.h"

int main(int argc, char *argv[])
{
	TS188 ts188;
	FILE *fp;		//视频文件
	char filename[256] = "1.ts";	//默认的视频文件名
	unsigned long long int *pf_position, f_position = 0;	//文件的当前位置
	pf_position = &f_position;

	unsigned char *p, temp[BUFFERLEN] = { 0 };	//文件流的临时缓冲区
	int offset_packet, bsize = 0;
	//int syn[2] = { 0 };  //检测文件的返回结果
	unsigned int packet_len = 0;	//当前文件的包长度
	unsigned int packet_position = 0;	//当前文件的偏移值
	struct ts_packet tsp;	//传输流分组层报头结构
	struct ts_pat_packet ts_pat;	//PAT表头结构

	/* 
	 * 如果没有输入文件名,使用默认文件名
	 */
	if (argc == 2)
		strcpy(filename, argv[1]);
	fp = fopen(filename, "rb");
	if (fp == NULL) {
		printf("文件打开失败,可能文件不存在\n");
		return -1;
	}

	bsize = fread(temp, sizeof(unsigned char), sizeof(temp), fp);
	printf("%s的%d字节被读取\n", filename, bsize);
	if (bsize > 188) {
		check188or204(bsize, temp, &packet_len, &packet_position);
		switch (packet_len) {
		case 0:
			printf("未找到同步\n");
			break;
		case 188:
		case 204:
			printf("检测该文件属于%d格式\n", packet_len);
			for (int i; i < 10; i++) {
				if (get_188_packet
				    (ts188, bsize, temp, &packet_position,
				     fp)) {
					print_ts(188, ts188);
				}
			}
			break;

		}
	}

	fclose(fp);
	return 0;
}
