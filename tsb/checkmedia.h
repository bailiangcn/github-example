/*
 * ==========================================================================
 *
 *       Filename:  checkmedia.h
 *
 *    Description:  checkmedia.c 的头文件
 *
 *        Version:  1.0
 *        Created:  2011年02月27日 11时52分29秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *        Company:  
 *
 * ==========================================================================
 */
#include <stdbool.h>

#ifndef CHECKMEDIA_H
#define CHECKMEDIA_H

#define BUFFERLEN 1024
#define SYNTIMES 3

typedef unsigned char TS188[188];
typedef unsigned char TS204[204];

/* 
 * 传输流分组层报头结构
 */
struct ts_packet {
	unsigned int sync_byte:8;
	unsigned int transport_error_indicator:1;
	unsigned int payload_unit_start_indicator:1;
	unsigned int transport_priority:1;
	unsigned long int pid:13;
	unsigned int transport_scrambling_control:2;
	unsigned int adaption_field_control:2;
	unsigned int continuity_counter:4;
};
/* 
 * PAT表头结构
 */
struct ts_pat_packet {
	unsigned int pointer_field:8;
	unsigned int table_id:8;
	unsigned int section_syntax_indicator:1;
	unsigned long int section_length:12;
	unsigned long int transport_stream_id:16;
	unsigned int version_number:5;
	unsigned int current_next_indicator:1;
	unsigned int section_number:8;
	unsigned int last_section_number:8;
	unsigned long int program_number:16;
	unsigned long int np_pid:13;
};

/* 
 *  Description:  判断一个数组是否是188或者204格式
 *                bsize 数组的长度
 *                temp  数组的实际数据指针
 *                返回一个数组res
 *				  packet_len = 0 文件未检测到同步
 *				  packet_len = 188 检测到188同步,起始位置 packet_position
 *				  packet_len = 204 检测到204同步,起始位置 packet_position
 */
void check188or204(int bsize, unsigned char *temp,
		   unsigned int *packet_len, unsigned int *packet_position);
/* 
 *  Description:  返回一个188字长的指针,如果当前包不在内存,自动读取文件
 */

bool get_188_packet(TS188 ts188, int order, int bsize, unsigned char *temp,
		    unsigned int *packet_position, FILE * fp);
/* 
 *  Description:  二进制显示一个8位的数字
 */
// void get_ts_packet(packet_len,)
void fb(unsigned c);
/* 
 *  Description:  用16进制方式显示二进制数据
 */
void print_ts(int bsize, unsigned char *data);
/* 
 *  Description:  解析一个ts包
 */
struct ts_packet split_ts(int bsize, unsigned char *data);

/* 
 *  Description:  打印一个ts包头
 */
void print_ts_head(struct ts_packet tsp);
/* 
 *  Description:  解析一个pat表头
 */
struct ts_pat_packet ana_ts_pat(int bsize, unsigned char *data);
/* 
 *  Description:  打印一个pat包头
 */
void print_pat_head(struct ts_pat_packet ts_pat);

/* 
 *  Description:  返回一个ts包
 *      f_position 文件的当前起点位置
 *      order 希望取得的第几个包
 *      res  res[0] 188 or 204  res[1] 偏移地址
 *      temp   内存字节
 *      fp  文件指针
 */
int get_ts_packet(unsigned long long int *pf_position, int order, int *res,
		  unsigned char *temp, FILE * fp);

#endif
