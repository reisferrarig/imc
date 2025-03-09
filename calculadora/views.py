from django.shortcuts import render
import re  # Para validar a entrada numérica

def home(request):
    imc = None
    categoria = None
    erro = None
    peso_ideal_min = None
    peso_ideal_max = None

    if request.method == 'POST':
        try:
            peso = float(request.POST['peso'])
            altura = request.POST['altura']

            # Substitui vírgula por ponto para permitir ambos os formatos
            altura = altura.replace(',', '.')

            # Remove caracteres não numéricos, exceto ponto
            altura = re.sub(r'[^0-9.]', '', altura)

            # Verifica se a altura é um número válido
            if not re.match(r'^\d+(\.\d{1,2})?$', altura):
                erro = "Por favor, insira um valor numérico válido para a altura (ex: 1.70 ou 1,70)."
            else:
                # Converte para float
                altura = float(altura)
           
            if altura > 3:
                altura = altura / 100
           
            # Validação de altura e peso
            if peso <= 0 or altura <= 0:
                erro = "Peso e altura devem ser positivos!"
            else:
                # Cálculo do IMC
                imc = peso / (altura ** 2)

                # Classificação do IMC
                if imc < 18.5:
                    categoria = 'Abaixo do peso'
                elif 18.5 <= imc < 24.9:
                    categoria = 'Peso normal'
                elif 25 <= imc < 29.9:
                    categoria = 'Sobrepeso'
                elif 30 <= imc < 34.9:
                    categoria = 'Obesidade Grau I'
                elif 35 <= imc < 39.9:
                    categoria = 'Obesidade Grau II'
                else:
                    categoria = 'Obesidade Grau III'

                # Cálculo do peso ideal
                peso_ideal_min = 18.5 * (altura ** 2)
                peso_ideal_max = 24.9 * (altura ** 2)

        except ValueError:
            erro = "Por favor, insira números válidos para peso e altura!"

    return render(request, 'calculadora/home.html', {
        'imc': imc, 
        'categoria': categoria, 
        'erro': erro, 
        'peso_ideal_min': peso_ideal_min, 
        'peso_ideal_max': peso_ideal_max
    })
