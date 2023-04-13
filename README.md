# Module
# Модуль по дисциплине "Языки и методы программирования"
Модуль для элементарной работы с матрицами

# Чем полезен наш модуль
Обработка реальных данных довольно часто осуществляется с помощью матриц. Большие данные удобнее всего вредставлять в виде массива, а его, в свою очередь, представлять в виде матрицы для дальнейших математиечских преобразований. Но именно сейчас операции с матрицами актуальны для нас как никогда. Вычислительная математика, графы, линейное программирование - всё осуществляется через матрицы. Например, в численных методах мы используем матричные операции во многих алгоритмах, каких как метод Якоби или прямой ход Гаусса. В компьютерной визуализации для 3D-графики матрицы используются для преобразования координат. Именно поэтому основные опреации с матрицами актуальны для нашего направления. Наш модуль позволяет использовать функции для основных математиечских операций с матрицами, благодаря чему пользователю не нужно самому писать код для той или иной операции - ему достаточно указать функцию и задать исходные параметры.


# Функции, которые способен выполнять наш модуль
- Умножение на скаляр
- Сложение/вычитание матриц
- Векторное умножение матрицы
- Транспонирование
- Вычисление определителя
- Вычисление обратной матрицы
- Умножение матриц

# Команда
- [Арина Вычегжанина](https://github.com/ArinaVychegzhanina)
- [Мария Воронина](https://github.com/MariVoronina)

# Необходимые библиотеки
Библиотека **Python.h** позволяет связать наш модуль с питоном. В ней используются методы и макросы, которые прдоставляют доступ к интерпретаторам из Python. А библеотека **math.h**, которая нужна для выполнения простых математических операций, используется у нас для команды fabs, которая применяется для данных типа float (команда abs в СИ для данных Python не применяется). 

```C
#include <Python.h>
#include <math.h>
```

### ***Умножение матрицы на скаляр***
```C
static PyObject* scalar_multiplication(PyObject* self, PyObject* args) {
  PyObject *listObj;
  double c;
  if( !PyArg_ParseTuple( args, "Od", &listObj, &c) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }

  Py_ssize_t lengthi = PyList_Size(listObj);
  PyObject* result = PyList_New(lengthi);  
  long i,j;
  Py_ssize_t lengthjpr = -1;

  for(i = 0; i < lengthi; i++){    
    PyObject* tempi = PyList_GetItem(listObj, i);
    Py_ssize_t lengthj = PyList_Size(tempi);
    if( lengthjpr == -1 ) {
      lengthjpr = lengthj;
    }
    else if ( lengthjpr != lengthj ){
      PyErr_SetString(PyExc_TypeError, "Invalid matrix !!!");
      return NULL;
    }
    PyObject* row = PyList_New(lengthj);
    for (j = 0; j <lengthj; j++){
       PyObject* tempj = PyList_GetItem(tempi, j);
       double elem = PyFloat_AsDouble(tempj);
       PyList_SetItem(row, j, PyFloat_FromDouble(c*elem)); 
    }
    PyList_SetItem(result, i, row);    
  }  
  
  return result;
}
```

