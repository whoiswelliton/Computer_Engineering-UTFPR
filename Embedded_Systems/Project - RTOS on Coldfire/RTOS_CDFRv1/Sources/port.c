#include "derivative.h"
#include "os.h"

/*A vantagem de utilizar um sistema operacional � que podemos trocar o processador e se 
tivermos o port nosso c�digo vai funcionar igual no outro processador, tudo o que depende
do sistema se mant�m, s� ser� modificado o port*/

/* PRIMEIRO PORT
	1. prepara a pilha da tarefa
	2. descobrir como gerar interrup��o de soffware nesse processador
	3. descobrir como salvar e restaurar contexto e mudar o tipo de processador
*/

/* Para implementar o Port devemos entender como s�o organizados os registradores desse processador:
- do D0 ao D7 = registradores de dados
- do A0 ao A7 =  registradores de endere�o
- o A7 � o stackpointer desse processador (32 bits)
- o PC s�o endere�os de 32 bits 

O banco de registradores � assim�trico.
*/

/*
INTERRUP��O = EXCESS�O
O stack frame de interrup��o:
- quando ocorre uma interrup��o, � salvo:
	1. a primeira coisa � o '(P)rogram (C)ounter', 
	2. depois registrador de status (32 bits)
	3. vetor com qual interrup��o que aconteceu
	4. o formato de empilhamento
	5. e um c�digo de erro (*que podemos ignorar)
*/

/*
GERENCIAMENTO DE TAREFAS
- O n�vel de interrup��o quando voltar de uma tarefa � 0, 0 � o n�vel da tarefa
- E quando estou dentro de uma interrup��o tenho que estar num n�vel "supervisor",ou seja, 
setar bit S para modo supervisor, isso � feito pra podermos mexer nos registradores 
que permitem realizar a troca de contexto.
*/

/*
TRAP = interrup��o de software do processador
- devemos disparar um yield() pra entender como ele salva contexo.
*/


/* Pra garantir que o sistema funciona, devemos escrever o nome do registrador quando
	 inicializada a tarefa, sabendo assim se conseguimos dispachar a tarefa corretamente*/
	 
cpu_t *stk_tmp;

cpu_t *PrepareStack(void *task, cpu_t *stk, int stk_size){
	stk = (cpu_t *)((int)stk + stk_size - sizeof(cpu_t)); 
	
	*stk-- = (cpu_t)task;
	*stk-- = 0x40002000;
	*stk-- = 0xA1;
	*stk-- = 0xA0;
	*stk-- = 0xD2;
	*stk-- = 0xD1;
	*stk-- = 0xD0;
	*stk-- = 0xA6;
	*stk-- = 0xA5;
	*stk-- = 0xA4;
	*stk-- = 0xA3;
	*stk-- = 0xA2;
	*stk-- = 0xD7;
	*stk-- = 0xD6;
	*stk-- = 0xD5;
	*stk-- = 0xD4;
	*stk = 0xD3;  
	
	return stk;
}

/*
Quando ocorre a interrup��o o compilador salva automaticamente e temos que salvar o complemento.

- Primeiro salvar todo o contexto, depois salvamos o que falta, usamos o SAVE_CONTEXT();
- Depois de corrigir o stackpointer pra nova tarefa, usamos o RESTORE_CONTEXT();

*/

/* - A Interrup��o de contexto ocorre na @Vtrap0 */
interrupt void SwitchContext(void){
	SAVE_CONTEXT();
	SAVE_SP();
	tcb[ct].stk = stk_tmp;
	stk_tmp = scheduler();
	RESTORE_SP();
	RESTORE_CONTEXT();
}

/* - A Interrup��o de tempo ocorre na @Vtpm1ovf */
interrupt void TickTimer(void){
	TPM1SC_TOF = 0;
	if( os_inc_and_compare()){
		SAVE_CONTEXT();
		SAVE_SP();
		tcb[ct].stk = stk_tmp;
		stk_tmp = scheduler();
		RESTORE_SP();
		RESTORE_CONTEXT();	
	}
}

void init_os_timer(void){
	TPM1SC = 0x00;
	TPM1MOD = 19999;
	TPM1SC = 0x48;
}