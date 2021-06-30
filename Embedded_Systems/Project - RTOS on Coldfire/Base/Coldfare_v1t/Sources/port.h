#ifndef _PORT_H_
#define _PORT_H_

/*long � o tipo do C que � garantidamente 32 bits*/
typedef unsigned long cpu_t;

extern cpu_t *stk_tmp;

cpu_t *PrepareStack(void *task, cpu_t *stk, int stk_size);
void init_os_timer(void);

/* INSTRU��ES DISPACHER:
	1. o stackpointer est� apontando para a pilha virtual da tarefa
	2. desempilhando, parte do contexto j� foi despachada
	3. corrigindo/reposicionando o stackpointer pra pegar a outra parte do contexto
	4. desempilhar o resto, o que j� foi salvo aturomaticamente
	5. corrigindo/reposicionando o stackpointer novamente
	6. instru��o de retorno de interrup��o, desempilha o registrador de status e o PC */
	
#define dispatcher()							\
		asm("MOVE stk_tmp, A7");				\
		asm("MOVEM.L (A7), D3-D7/A2-A6");		\
		asm("LEA 40(A7), A7");					\
		asm("MOVEM.L (A7), D0-D2/A0-A1");		\
		asm("LEA 20(A7), A7");					\
		asm("RTE") 							
	 	
#define yield()	asm("TRAP %0")	

/* SAVE_SP + SAVE_CONTEXT + RESTORE_CONTEXT + RESTORE_SP
S�o constru�das a partir das intru��es j� utilizadas anteriormente no dispacher()	
Pois, temos que salvar e restaurar n�o s� o stack pointer,tamb�m temos que salvar e restaurar o contexto adicional

SAVE_CONTEXT � o inverso da RESTORE_CONTEXT

*/				

#define SAVE_SP() asm("MOVE A7, stk_tmp")			

#define SAVE_CONTEXT()							\
		asm("LEA -40(A7), A7");					\
		asm("MOVEM.L D3-D7/A2-A6, (A7)")					
	
#define RESTORE_CONTEXT()						\
		asm("MOVEM.L (A7), D3-D7/A2-A6");    	\
		asm("LEA 40(A7), A7")							
	
#define RESTORE_SP() asm("MOVE stk_tmp, A7")

#endif