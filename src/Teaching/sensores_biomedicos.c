// Lógica para Microcontrolador (Ex: monitorando batimentos)
float alpha = 0.1;
float valorFiltrado = 0;

void loop() {
    int leituraBruta = analogRead(A0);
    // Filtro em tempo real (EMA - Exponential Moving Average)
    valorFiltrado = (alpha * leituraBruta) + (1.0 - alpha) * valorFiltrado;
    
    if (valorFiltrado > limiar_batimento) {
        detectarPulso();
    }
}
