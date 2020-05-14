import math
import scipy
from scipy.special import erf
from decimal import Decimal


def reduce_fraction(n, m):
    k = math.gcd(n, m)
    return str(n // k) + '/' + str(m // k)


def count_permutation(n):
    return math.factorial(n)


def count_placement(n, k):
    return math.factorial(n) // math.factorial(n - k)


def count_combinations(n, k):
    return math.factorial(n) // (math.factorial(n - k) * math.factorial(k))


def bernulli(n, k, p):
    if p >= 0:
        return count_combinations(n, k) * (p ** k) * ((1-p) ** (n-k))
    else:
        return count_combinations(n, k) * ((1 + p) ** k) * ((-1 * p) ** (n-k))


def laplas_arg(k, n, p):
    return (k - n * p) / (math.sqrt(n * p * (1 - p)))


def local_laplas(x):
    return (1/(math.sqrt(2*math.pi))) * math.exp(-1 * x * x / 2)


def integral_laplas(x):
    return erf(x / 2 ** 0.5) / 2


def puasson(k, n, p):
    return (n * p) ** k * math.exp(-n * p) / math.factorial(k)


def ver_count_event_solve(n, p, k, k2=None):
    msg = ['✅*Решение*']

    if k2 is None:
        if n >= 10:
            if p <= 0.1 and k < 20:
                answ = str(puasson(k, n, p))
                msg.append('Для решения данной задачи лучше всего подходит формула Пуассона, '
                           'так количество испытаний велико, а вероятность достаточно маленькая '
                           'величина.')
                msg.append('λ = np = ' + str(n) + '⋅' + str(p) + ' = ' + str(n*p))
                msg.append('P' + str(n) + '(' + str(k) + ') = λ^k⋅e^-λ / k! = ' + answ)
            else:
                x = laplas_arg(k, n, p)
                answ = str(local_laplas(x))
                msg.append('Данную задачу лучше всего решать с помощью локальной теоремы Лапласа.')
                msg.append('q = 1 - p = ' + str(1-p))
                msg.append('x = (k - np) / √(npq) = ' + str(x))
                msg.append('P' + str(n) + '(' + str(k) + ') = φ(x) = ' + answ +
                           ' (я нашёл это значение из '
                           '[таблицы](http://www.ekonomika-st.ru/drugie/metodi/t-ver-1-4-0.html#1))')
        else:
            answ = str(bernulli(n, k, p))
            msg.append('Попробуем найти решение с помощью формулы Бернулли:')
            msg.append('P' + str(n) + '(' + str(k) + ') = ' + 'C(k, n)⋅p^k⋅q^(n-k) = ' + answ)
    else:
        answ = 0
        if k2 - k > 5:
            x1 = laplas_arg(k, n, p)
            x2 = laplas_arg(k2, n, p)
            answ = str(abs(integral_laplas(x2) - integral_laplas(x1)))
            msg.append('Чтобы облегчить расчёты посчитаем вероятность с помощью интегральной теоремы Лапласа.')
            msg.append('x1 = (k1 - np) / √(npq) = ' + str(x1))
            msg.append('x2 = (k2 - np) / √(npq) = ' + str(x2))
            msg.append('P' + str(n) + '(' + str(k) + ' <= k <= ' + str(k2) + ') = Φ(x2) - Φ(x1) = ' + answ +
                       ' (я нашёл это значение интегральной функции Лапласа из '
                       '[таблицы](http://www.ekonomika-st.ru/drugie/metodi/t-ver-1-4-0.html#2))')
        elif n >= 10:
            if p <= 0.1 and k < 10:
                msg.append('Для решения данной задачи лучше всего подходит формула Пуассона, '
                           'так количество испытаний велико, а вероятность достаточно маленькая '
                           'величина.')
                msg.append('λ = np = ' + str(n) + '⋅' + str(p) + ' = ' + str(n * p))
                for i in range(k, k2 + 1):
                    lansw = puasson(i, n, p)
                    msg.append('P' + str(n) + '(' + str(i) + ') = λ^k⋅e^-λ / k! = ' + str(lansw))
                    answ += lansw
                msg.append('P' + str(n) + '(' + str(k) + ' <= k <= ' + str(k2) + ') = ∑Pn(i) = ' + str(answ))
            else:
                msg.append('Данную задачу лучше всего решать с помощью локальной теоремы Лапласа.')
                msg.append('q = 1 - p = ' + str(1 - p))
                for i in range(k, k2 + 1):
                    msg.append('k = ' + str(i))
                    x = laplas_arg(i, n, p)
                    msg.append('x = (k - np) / √(npq) = ' + str(x))
                    lansw = local_laplas(x)
                    msg.append('P' + str(n) + '(' + str(k) + ') = φ(x) = ' + str(lansw))
                    answ += lansw
                msg.append('Значения функции Лапласа я брал из '
                           '[таблицы](http://www.ekonomika-st.ru/drugie/metodi/t-ver-1-4-0.html#1).')
                msg.append('P' + str(n) + '(' + str(k) + ' <= k <= ' + str(k2) + ') = ∑Pn(i) = ' + str(answ))
        else:
            msg.append('Попробуем найти решение с помощью формулы Бернулли:')
            for i in range(k, k2 + 1):
                lansw = bernulli(n, i, p)
                msg.append('P' + str(n) + '(' + str(i) + ') = ' + 'C(k, n)⋅p^k⋅q^(n-k) = ' + str(lansw))
                answ += lansw
            msg.append('P' + str(n) + '(' + str(k) + ' <= k <= ' + str(k2) + ') = ∑Pn(i) = ' + str(answ))
    msg.append('*Ответ: ' + str(answ) + '*')
    return '\n'.join(msg)


def most_probable_count(n, p):
    q = 1 - p
    x = n * p - q
    if x != int(x):
        return str(math.ceil(x))
    else:
        return str(int(x)) + ' и ' + str(int(x+1))


def math_expectation(p, x):
    m = Decimal(0)
    for i in range(len(x)):
        m += Decimal(p[i]) * Decimal(x[i])
    return float(m)


def dispersion(p, x):
    x2 = list(map(lambda a: math.pow(a, 2), x))
    return math_expectation(p, x2) - (math.pow(math_expectation(p, x), 2))


def mean_square_deviation(p, x):
    return math.sqrt(dispersion(p, x))
