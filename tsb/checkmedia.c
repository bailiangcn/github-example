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

#define BUFFERLEN 1880
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

void fb(unsigned c)
{
	for (int i = 0; i < 8; i++) {
		if (i % 8 == 4)
			printf(" ");
		putchar(((c & 1 << 7) == 0) ? '0' : '1');
		c <<= 1;
	}
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  print_ts
 *  Description:  用16进制方式显示二进制数据
 * =====================================================================================
 */
void print_ts(int bsize, unsigned char *data)
{
	for (int i = 0; i < bsize; i++) {
		if (data[i] != 0xff) {
			printf("%2d==>0x%02x (", i, data[i]);
			fb(data[i]);
			printf(")\n");
		}
	}
	printf("\n");
}

void split_ts(int bsize, unsigned char *data)
{
	struct ts_first {
		unsigned int transport_error_indicator:1;
		unsigned int payload_unit_start_indicator:1;
		unsigned int transport_priority:1;
		unsigned long int pid:13;
		unsigned int transport_scrambling_control:2;
		unsigned int adaption_field_control:2;
		unsigned int continuity_counter:4;
	} tsp;
	unsigned char tempindi = 0;
	printf("解析开始:\n");
	if (data[0] == 0x47) {
		printf("同步正常\n");
	} else {
		printf("同步失败\n");
		return;
	}
	tsp.transport_error_indicator = (data[1] & (1 << 7)) ? 1 : 0;
	tsp.payload_unit_start_indicator = (data[1] & (1 << 6)) ? 1 : 0;
	tsp.transport_priority = (data[1] & (1 << 5));
	tsp.pid = data[1] & 0x1F;
	tsp.pid = tsp.pid << 8 + data[2];
	tsp.transport_scrambling_control = ((data[3] >> 6) & 0x3);
	tsp.adaption_field_control = ((data[3] >> 4) & 0x3);
	tsp.continuity_counter = (data[3] & 0xF);

	printf("transport_error_indicator:%d\n", tsp.transport_error_indicator);
	printf("payload_unit_start_indicator:%d\n",
	       tsp.payload_unit_start_indicator);
	printf("tarnsport_priority:%d\n", tsp.transport_priority);
	printf("tarnsport_pid:0x%02x\n", tsp.pid);
	printf("transport_scrambling_control:%d\n",
	       tsp.transport_scrambling_control);
	printf("adaption_field_control:%d\n", tsp.adaption_field_control);
	printf("continuity_counter:%d\n", tsp.continuity_counter);

	if (tsp.pid == 0x00) {
		printf("pat 表格:\n");
		unsigned long int tempval = 0, tempvala;
		tempval = data[4];
		printf("pointer_field:%ld\n", tempval);
		tempval = data[5];
		printf("table_id:%lx\n", tempval);
		tempval = (data[6] & (1 << 7)) ? 1 : 0;
		printf("section_syntax_indicator:%lx\n", tempval);
		tempval = (data[6] & 0x0F) << 8;
		tempval = tempval + data[7];
		printf("section_length:%ld\n", tempval);
		tempval = (data[8] << 8) + data[9];
		printf("transport_stream_id:%ld\n", tempval);
		tempval = (data[10] >> 1) & 0x1F;
		printf("version_number:%ld\n", tempval);
		tempval = data[10] & 0x1;
		printf("current_next_indicator:%ld\n", tempval);
		tempval = data[11];
		printf("section_number:%ld\n", tempval);
		tempval = data[12];
		printf("last_section_number:%ld\n", tempval);
		tempval = (data[13] << 8) + data[14];
		printf("program_number:%ld\n", tempval);
		tempvala = ((data[15] & 0x1F) << 8) + data[16];
		if (tempval == 0x00)
			printf("network_PID:%ld\n", tempvala);
		else
			printf("program_map_PID:%ld\n", tempvala);
		printf("CRC:0x%02x%02x%02x%02x", data[17], data[18], data[19],
		       data[20]);
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
	unsigned char *p, temp[BUFFERLEN] = {
		0
	};
	int offset_packet, bsize = 0;
	char filename[256] = "1.ts";
	int syn[2] = {
		0
	};
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
			printf("第%d个包:\n", offset_packet);
			p = &temp[syn[1] + syn[0] * offset_packet];
			print_ts(syn[0], p);
			split_ts(syn[0], p);
			break;
		}
	}

	fclose(fp);
	return 0;
}
