#include <iostream>
#include <iomanip>
#include <string>
#include <limits>
#include <fstream>
#include <sstream>

using namespace std;

// Limite maximo de contas e movimentacoes
const int MAX_CONTAS = 100;
const int MAX_MOVIMENTACOES = 500;

// Arrays para armazenar as contas
int numeroConta[MAX_CONTAS];
string nomeCliente[MAX_CONTAS];
string cpf[MAX_CONTAS];
int tipoConta[MAX_CONTAS];
double saldo[MAX_CONTAS];
bool contaAtiva[MAX_CONTAS];

// Arrays para armazenar as movimentacoes
int contaMovimentacao[MAX_MOVIMENTACOES];
char tipoMovimentacao[MAX_MOVIMENTACOES];
double valorMovimentacao[MAX_MOVIMENTACOES];

// Quantidade de contas e movimentacoes
int quantidadeContas = 0;
int quantidadeMovimentacoes = 0;

// ==========================================
// FUNCOES DE MANIPULACAO DE ARQUIVOS
// ==========================================

// Carrega as contas do arquivo
void carregarContas() {

    ifstream arquivo("contas.txt");

    if (!arquivo.is_open()) {
        return;
    }

    string linha;

    while (getline(arquivo, linha)) {

        if (quantidadeContas >= MAX_CONTAS) {
            break;
        }

        stringstream fluxo(linha);

        string numero, nome, documento;
        string tipo, valor, situacao;

        if (!getline(fluxo, numero, ';') ||
            !getline(fluxo, nome, ';') ||
            !getline(fluxo, documento, ';') ||
            !getline(fluxo, tipo, ';') ||
            !getline(fluxo, valor, ';') ||
            !getline(fluxo, situacao)) {

            continue;
        }

        try {

            int posicao = quantidadeContas;

            numeroConta[posicao] = stoi(numero);
            nomeCliente[posicao] = nome;
            cpf[posicao] = documento;
            tipoConta[posicao] = stoi(tipo);
            saldo[posicao] = stod(valor);
            contaAtiva[posicao] = (stoi(situacao) != 0);

            quantidadeContas++;

        } catch (...) {
            continue;
        }
    }

    arquivo.close();
}

// Salva todas as contas no arquivo
void salvarContas() {

    ofstream arquivo("contas.txt");

    if (arquivo.is_open()) {

        arquivo << fixed << setprecision(2);

        for (int i = 0; i < quantidadeContas; i++) {

            arquivo << numeroConta[i] << ";"
                    << nomeCliente[i] << ";"
                    << cpf[i] << ";"
                    << tipoConta[i] << ";"
                    << saldo[i] << ";"
                    << contaAtiva[i] << endl;
        }

        arquivo.close();

    } else {
        cout << "Erro ao salvar o arquivo de contas.\n";
    }
}

// Carrega as movimentacoes do arquivo
void carregarMovimentacoes() {

    ifstream arquivo("movimentacoes.txt");

    if (!arquivo.is_open()) {
        return;
    }

    string linha;

    while (getline(arquivo, linha)) {

        if (quantidadeMovimentacoes >= MAX_MOVIMENTACOES) {
            break;
        }

        stringstream fluxo(linha);

        string numero, tipo, valor;

        if (!getline(fluxo, numero, ';') ||
            !getline(fluxo, tipo, ';') ||
            !getline(fluxo, valor)) {

            continue;
        }

        try {

            contaMovimentacao[quantidadeMovimentacoes] = stoi(numero);
            tipoMovimentacao[quantidadeMovimentacoes] = tipo[0];
            valorMovimentacao[quantidadeMovimentacoes] = stod(valor);

            quantidadeMovimentacoes++;

        } catch (...) {
            continue;
        }
    }

    arquivo.close();
}

// Salva todas as movimentacoes no arquivo
void salvarMovimentacoes() {

    ofstream arquivo("movimentacoes.txt");

    if (arquivo.is_open()) {

        arquivo << fixed << setprecision(2);

        for (int i = 0; i < quantidadeMovimentacoes; i++) {

            arquivo << contaMovimentacao[i] << ";"
                    << tipoMovimentacao[i] << ";"
                    << valorMovimentacao[i] << endl;
        }

        arquivo.close();

    } else {
        cout << "Erro ao salvar o arquivo de movimentacoes.\n";
    }
}

// ==========================================
// PROGRAMA PRINCIPAL
// ==========================================

int main() {

    int opcao;

    cout << fixed << setprecision(2);

    // Carrega os dados armazenados nos arquivos
    carregarContas();
    carregarMovimentacoes();

    cout << "\n====================================\n";
    cout << "       SISTEMA BANCARIO\n";
    cout << "====================================\n";

    cout << "Contas carregadas: " << quantidadeContas << endl;
    cout << "Movimentacoes carregadas: "
         << quantidadeMovimentacoes << endl;

    // Menu principal
    do {

        cout << "\n====================================\n";
        cout << "       SISTEMA BANCARIO\n";
        cout << "====================================\n";
        cout << "1 - Cadastrar conta\n";
        cout << "2 - Listar contas\n";
        cout << "3 - Consultar conta\n";
        cout << "4 - Realizar deposito\n";
        cout << "5 - Realizar saque\n";
        cout << "6 - Realizar transferencia\n";
        cout << "7 - Exibir extrato\n";
        cout << "0 - Sair\n";
        cout << "====================================\n";
        cout << "Escolha uma opcao: ";
        cin >> opcao;

        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        switch (opcao) {

            // 1 - CADASTRAR CONTA
            case 1: {

                if (quantidadeContas >= MAX_CONTAS) {
                    cout << "\nLimite de contas atingido!\n";
                    break;
                }

                int numero;
                bool existe = false;

                cout << "\nDigite o numero da conta: ";
                cin >> numero;

                if (numero <= 0) {
                    cout << "Numero de conta invalido!\n";
                    break;
                }

                // Verifica se a conta ja existe
                for (int i = 0; i < quantidadeContas; i++) {

                    if (numeroConta[i] == numero) {
                        existe = true;
                    }
                }

                if (existe) {
                    cout << "Essa conta ja esta cadastrada!\n";
                    break;
                }

                numeroConta[quantidadeContas] = numero;

                cin.ignore(numeric_limits<streamsize>::max(), '\n');

                cout << "Nome do cliente: ";
                getline(cin, nomeCliente[quantidadeContas]);

                cout << "CPF do cliente: ";
                getline(cin, cpf[quantidadeContas]);

                cout << "Tipo de conta (1 - Corrente / 2 - Poupanca): ";
                cin >> tipoConta[quantidadeContas];

                if (tipoConta[quantidadeContas] != 1 &&
                    tipoConta[quantidadeContas] != 2) {

                    cout << "Tipo de conta invalido!\n";
                    break;
                }

                // Toda conta comeca com saldo zero
                saldo[quantidadeContas] = 0.0;
                contaAtiva[quantidadeContas] = true;

                quantidadeContas++;

                // ETAPA 3: Salva as contas no arquivo
                salvarContas();

                cout << "\nConta cadastrada com sucesso!\n";

                break;
            }

            // 2 - LISTAR CONTAS
            case 2: {

                cout << "\n===== CONTAS CADASTRADAS =====\n";

                if (quantidadeContas == 0) {
                    cout << "Nenhuma conta cadastrada.\n";
                    break;
                }

                for (int i = 0; i < quantidadeContas; i++) {

                    if (contaAtiva[i]) {

                        cout << "\nNumero: " << numeroConta[i];
                        cout << "\nCliente: " << nomeCliente[i];
                        cout << "\nCPF: " << cpf[i];

                        if (tipoConta[i] == 1) {
                            cout << "\nTipo: Corrente";
                        } else {
                            cout << "\nTipo: Poupanca";
                        }

                        cout << "\nSaldo: R$ " << saldo[i] << endl;
                        cout << "Situacao: Ativa\n";
                        cout << "-----------------------------\n";
                    }
                }

                break;
            }

            // 3 - CONSULTAR CONTA
            case 3: {

                int numero;
                int indice = -1;

                cout << "\nDigite o numero da conta: ";
                cin >> numero;

                // Procura a conta
                for (int i = 0; i < quantidadeContas; i++) {

                    if (numeroConta[i] == numero && contaAtiva[i]) {
                        indice = i;
                        break;
                    }
                }

                if (indice == -1) {
                    cout << "Conta nao encontrada!\n";
                } else {

                    cout << "\n===== DADOS DA CONTA =====\n";
                    cout << "Numero: " << numeroConta[indice] << endl;
                    cout << "Cliente: " << nomeCliente[indice] << endl;
                    cout << "CPF: " << cpf[indice] << endl;

                    if (tipoConta[indice] == 1) {
                        cout << "Tipo: Corrente\n";
                    } else {
                        cout << "Tipo: Poupanca\n";
                    }

                    cout << "Saldo: R$ " << saldo[indice] << endl;
                    cout << "Situacao: Ativa\n";
                }

                break;
            }

            // 4 - REALIZAR DEPOSITO
            case 4: {

                int numero;
                int indice = -1;
                double valor;

                cout << "\nDigite o numero da conta: ";
                cin >> numero;

                // Localiza a conta
                for (int i = 0; i < quantidadeContas; i++) {

                    if (numeroConta[i] == numero && contaAtiva[i]) {
                        indice = i;
                        break;
                    }
                }

                if (indice == -1) {
                    cout << "Conta nao encontrada!\n";
                    break;
                }

                cout << "Digite o valor do deposito: R$ ";
                cin >> valor;

                if (valor <= 0) {
                    cout << "Valor invalido!\n";
                    break;
                }

                if (quantidadeMovimentacoes >= MAX_MOVIMENTACOES) {
                    cout << "Limite de movimentacoes atingido!\n";
                    break;
                }

                // Atualiza o saldo
                saldo[indice] = saldo[indice] + valor;

                // Registra a movimentacao
                contaMovimentacao[quantidadeMovimentacoes] =
                    numeroConta[indice];

                tipoMovimentacao[quantidadeMovimentacoes] = 'D';

                valorMovimentacao[quantidadeMovimentacoes] = valor;

                quantidadeMovimentacoes++;

                // ETAPA 3: Atualiza os arquivos
                salvarContas();
                salvarMovimentacoes();

                cout << "\nDeposito realizado com sucesso!\n";
                cout << "Novo saldo: R$ " << saldo[indice] << endl;

                break;
            }

            // 5 - REALIZAR SAQUE
            case 5: {

                int numero;
                int indice = -1;
                double valor;

                cout << "\nDigite o numero da conta: ";
                cin >> numero;

                // Localiza a conta
                for (int i = 0; i < quantidadeContas; i++) {

                    if (numeroConta[i] == numero && contaAtiva[i]) {
                        indice = i;
                        break;
                    }
                }

                if (indice == -1) {
                    cout << "Conta nao encontrada!\n";
                    break;
                }

                cout << "Digite o valor do saque: R$ ";
                cin >> valor;

                if (valor <= 0) {
                    cout << "Valor invalido!\n";
                    break;
                }

                if (valor > saldo[indice]) {
                    cout << "Saldo insuficiente!\n";
                    break;
                }

                if (quantidadeMovimentacoes >= MAX_MOVIMENTACOES) {
                    cout << "Limite de movimentacoes atingido!\n";
                    break;
                }

                // Atualiza o saldo
                saldo[indice] = saldo[indice] - valor;

                // Registra a movimentacao
                contaMovimentacao[quantidadeMovimentacoes] =
                    numeroConta[indice];

                tipoMovimentacao[quantidadeMovimentacoes] = 'S';

                valorMovimentacao[quantidadeMovimentacoes] = valor;

                quantidadeMovimentacoes++;

                // ETAPA 3: Atualiza os arquivos
                salvarContas();
                salvarMovimentacoes();

                cout << "\nSaque realizado com sucesso!\n";
                cout << "Novo saldo: R$ " << saldo[indice] << endl;

                break;
            }

            // 6 - REALIZAR TRANSFERENCIA
            case 6: {

                int origem, destino;
                int indiceOrigem = -1;
                int indiceDestino = -1;
                double valor;

                cout << "\nConta de origem: ";
                cin >> origem;

                cout << "Conta de destino: ";
                cin >> destino;

                // Localiza as duas contas
                for (int i = 0; i < quantidadeContas; i++) {

                    if (numeroConta[i] == origem && contaAtiva[i]) {
                        indiceOrigem = i;
                    }

                    if (numeroConta[i] == destino && contaAtiva[i]) {
                        indiceDestino = i;
                    }
                }

                if (indiceOrigem == -1 || indiceDestino == -1) {
                    cout << "Uma ou ambas as contas nao foram encontradas!\n";
                    break;
                }

                if (indiceOrigem == indiceDestino) {
                    cout << "Nao e possivel transferir para a mesma conta!\n";
                    break;
                }

                cout << "Digite o valor da transferencia: R$ ";
                cin >> valor;

                if (valor <= 0) {
                    cout << "Valor invalido!\n";
                    break;
                }

                if (valor > saldo[indiceOrigem]) {
                    cout << "Saldo insuficiente!\n";
                    break;
                }

                // A transferencia precisa de dois registros
                if (quantidadeMovimentacoes + 2 > MAX_MOVIMENTACOES) {
                    cout << "Espaco insuficiente no historico!\n";
                    break;
                }

                // Atualiza os saldos
                saldo[indiceOrigem] = saldo[indiceOrigem] - valor;

                saldo[indiceDestino] = saldo[indiceDestino] + valor;

                // Registra a saida da conta de origem
                contaMovimentacao[quantidadeMovimentacoes] =
                    numeroConta[indiceOrigem];

                tipoMovimentacao[quantidadeMovimentacoes] = 'S';

                valorMovimentacao[quantidadeMovimentacoes] = valor;

                quantidadeMovimentacoes++;

                // Registra a entrada na conta de destino
                contaMovimentacao[quantidadeMovimentacoes] =
                    numeroConta[indiceDestino];

                tipoMovimentacao[quantidadeMovimentacoes] = 'D';

                valorMovimentacao[quantidadeMovimentacoes] = valor;

                quantidadeMovimentacoes++;

                // ETAPA 3: Atualiza os arquivos
                salvarContas();
                salvarMovimentacoes();

                cout << "\nTransferencia realizada com sucesso!\n";
                cout << "Saldo da conta de origem: R$ "
                     << saldo[indiceOrigem] << endl;

                cout << "Saldo da conta de destino: R$ "
                     << saldo[indiceDestino] << endl;

                break;
            }

            // 7 - EXIBIR EXTRATO
            case 7: {

                int numero;
                int indice = -1;
                bool encontrou = false;

                double entradas = 0.0;
                double saidas = 0.0;

                cout << "\nDigite o numero da conta: ";
                cin >> numero;

                // Verifica se a conta existe
                for (int i = 0; i < quantidadeContas; i++) {

                    if (numeroConta[i] == numero && contaAtiva[i]) {
                        indice = i;
                        break;
                    }
                }

                if (indice == -1) {
                    cout << "Conta nao encontrada!\n";
                    break;
                }

                cout << "\n===== EXTRATO BANCARIO =====\n";
                cout << "Conta: " << numeroConta[indice] << endl;
                cout << "Cliente: " << nomeCliente[indice] << endl;

                cout << "-----------------------------\n";

                // Percorre o historico de movimentacoes
                for (int i = 0; i < quantidadeMovimentacoes; i++) {

                    if (contaMovimentacao[i] == numero) {

                        encontrou = true;

                        if (tipoMovimentacao[i] == 'D') {

                            cout << "Deposito/Entrada: + R$ "
                                 << valorMovimentacao[i] << endl;

                            entradas += valorMovimentacao[i];

                        } else if (tipoMovimentacao[i] == 'S') {

                            cout << "Saque/Saida: - R$ "
                                 << valorMovimentacao[i] << endl;

                            saidas += valorMovimentacao[i];
                        }
                    }
                }

                if (!encontrou) {
                    cout << "Nenhuma movimentacao encontrada.\n";
                }

                cout << "-----------------------------\n";
                cout << "Total de entradas: R$ " << entradas << endl;
                cout << "Total de saidas: R$ " << saidas << endl;
                cout << "Saldo atual: R$ " << saldo[indice] << endl;

                break;
            }

            // 0 - SAIR DO SISTEMA
            case 0:

                cout << "\nSistema encerrado. Obrigado!\n";

                break;

            default:

                cout << "\nOpcao invalida! Tente novamente.\n";
        }

    } while (opcao != 0);

    return 0;
}
