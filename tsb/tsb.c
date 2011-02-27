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
	FILE *fp;
	unsigned long long int *pf_position, f_position = 0;
	pf_position = &f_position;
	unsigned char *p, temp[BUFFERLEN] = { 0 };
	int offset_packet, bsize = 0;
	char filename[256] = "1.ts";
	int syn[2] = { 0 };
	struct ts_packet tsp;
	struct ts_pat_packet ts_pat;

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
			printf("第%d个包:\n", offset_packet);
			p = &temp[syn[1] + syn[0] * offset_packet];
			print_ts(syn[0], p);
			tsp = split_ts(syn[0], p);
			if (tsp.sync_byte == 0x47)
				print_ts_head(tsp);
			else
				break;
			if (tsp.pid == 0x00) {
				ts_pat = ana_ts_pat(syn[0], p);
				if (ts_pat.table_id == 0x00)
					print_pat_head(ts_pat);
			}
			break;

		}
		if (get_ts_packet(pf_position, 0, syn, temp, fp) == 0)
			print_ts(syn[0], p);
	}

	fclose(fp);
	return 0;
}
