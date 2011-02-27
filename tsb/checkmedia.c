/*
 * ==========================================================================
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
 * ==========================================================================
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "checkmedia.h"

/* 
 * ===  FUNCTION  ===========================================================
 *         Name:  check188or204
 *  Description:  判断一个数组是否是188或者204格式
 *                bsize 数组的长度
 *                temp  数组的实际数据指针
 *				  返回一个数组res
 *				  res[0] = 0 文件未检测到同步
 *				  res[0] = 188 检测到188同步,起始位置 res[1]
 *				  res[0] = 204 检测到204同步,起始位置 res[1]
 * ==========================================================================
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

/* 
 * ===  FUNCTION  ===========================================================
 *         Name:  fb
 *  Description:  二进制显示一个8位的数字
 * ==========================================================================
 */
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
 * ===  FUNCTION  ===========================================================
 *         Name:  print_ts
 *  Description:  用16进制方式显示二进制数据
 * ==========================================================================
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

/* 
 * ===  FUNCTION  ===========================================================
 *         Name:  split_ts
 *  Description:  解析一个ts包,返回一个包头结构
 * ==========================================================================
 */
struct ts_packet split_ts(int bsize, unsigned char *data)
{
	struct ts_packet tsp;
	unsigned char tempindi = 0;
	printf("解析开始:\n");
	if (data[0] == 0x47) {
		tsp.sync_byte = 0x47;
	} else {
		printf("同步失败\n");
		tsp.sync_byte = 0;
		return tsp;
	}
	/* 
	 * 对包头部分进行解析
	 */
	tsp.transport_error_indicator = (data[1] & (1 << 7)) ? 1 : 0;
	tsp.payload_unit_start_indicator = (data[1] & (1 << 6)) ? 1 : 0;
	tsp.transport_priority = (data[1] & (1 << 5));
	tsp.pid = data[1] & 0x1F;
	tsp.pid = tsp.pid << 8 + data[2];
	tsp.transport_scrambling_control = ((data[3] >> 6) & 0x3);
	tsp.adaption_field_control = ((data[3] >> 4) & 0x3);
	tsp.continuity_counter = (data[3] & 0xF);
	/* 
	 * 对实际携带数据进行解析
	 */
	return tsp;
}

/* 
 * ===  FUNCTION  ============================================================
 *         Name:  ana_ts_pat
 *  Description:  解析pat表格
 * ===========================================================================
 */
struct ts_pat_packet ana_ts_pat(int bsize, unsigned char *data)
{

	struct ts_packet tsp;
	struct ts_pat_packet ts_pat;

	tsp = split_ts(bsize, data);
	if (tsp.pid == 0x00) {
		ts_pat.pointer_field = data[4];
		ts_pat.table_id = data[5];
		ts_pat.section_syntax_indicator = (data[6] & (1 << 7)) ? 1 : 0;
		ts_pat.section_length = (data[6] & 0x0F) << 8;
		ts_pat.section_length = ts_pat.section_length + data[7];
		ts_pat.transport_stream_id = (data[8] << 8) + data[9];
		ts_pat.version_number = (data[10] >> 1) & 0x1F;
		ts_pat.current_next_indicator = data[10] & 0x1;
		ts_pat.section_number = data[11];
		ts_pat.last_section_number = data[12];
		ts_pat.program_number = (data[13] << 8) + data[14];
		ts_pat.np_pid = ((data[15] & 0x1F) << 8) + data[16];
/* 		printf("CRC:0x%02x%02x%02x%02x\n", data[17], data[18], data[19],
 * 		       data[20]);
 */
	} else {
		ts_pat.table_id = 0xff;
	}
	return ts_pat;
}

/* 
 * ===  FUNCTION  ============================================================
 *         Name:  print_ts_head
 *  Description:  打印ts表头结构
 * ===========================================================================
 */
void print_ts_head(struct ts_packet tsp)
{

	printf("ts表头结构:\n");
	printf("transport_error_indicator:%d\n", tsp.transport_error_indicator);
	printf("payload_unit_start_indicator:%d\n",
	       tsp.payload_unit_start_indicator);
	printf("tarnsport_priority:%d\n", tsp.transport_priority);
	printf("tarnsport_pid:0x%02x\n", tsp.pid);
	printf("transport_scrambling_control:%d\n",
	       tsp.transport_scrambling_control);
	printf("adaption_field_control:%d\n", tsp.adaption_field_control);
	printf("continuity_counter:%d\n", tsp.continuity_counter);
}

/* 
 * ===  FUNCTION  ============================================================
 *         Name:  print_pat_head
 *  Description:  打印pat表格结构
 * ===========================================================================
 */
void print_pat_head(struct ts_pat_packet ts_pat)
{
	printf("pat 表格:\n");
	printf("pointer_field:%d\n", ts_pat.pointer_field);
	printf("table_id:%x\n", ts_pat.table_id);
	printf("section_syntax_indicator:%x\n",
	       ts_pat.section_syntax_indicator);
	printf("section_length:%d\n", ts_pat.section_length);
	printf("transport_stream_id:%d\n", ts_pat.transport_stream_id);
	printf("version_number:%d\n", ts_pat.version_number);
	printf("current_next_indicator:%d\n", ts_pat.current_next_indicator);
	printf("section_number:%d\n", ts_pat.section_number);
	printf("last_section_number:%d\n", ts_pat.last_section_number);
	printf("program_number:%d\n", ts_pat.program_number);
	if (ts_pat.program_number == 0x00)
		printf("network_PID:%d\n", ts_pat.np_pid);
	else
		printf("program_map_PID:%d\n", ts_pat.np_pid);
}

/* 
 * ===  FUNCTION  ============================================================
 *         Name:  get_ts_packet
 *  Description:  返回指定顺序的ts的包,如果不在内存当中自动读文件
 *		返回值： -1 表示没有找到合适的包
 *				 0  表示找到了合适的包
 * ===========================================================================
 */
int get_ts_packet(unsigned long long int *pf_position, int order, int *res,
		  unsigned char *temp, FILE * fp)
{
	printf("beging get ts packet");
	return 0;
}
