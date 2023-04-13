# Module
# Модуль по дисциплине "Языки и методы программирования"
Модуль для работы с матрицами

# Описание проекта


### ***Правила работы с приложением***

# Список задач
- Сгенерировать данные по коттеджам с помощью бибилиотеки Faker для дальнейшей работы с ними
- Реализовать функционал нашего приложения
- Реализовать интерфейс нашего приложения

# Команда
- [Арина Вычегжанина](https://github.com/ArinaVychegzhanina)
- [Мария Воронина](https://github.com/MariVoronina)

# Необходимые библиотеки
Библиотека **Python.h** позволяет связать наш модуль с питоном. В ней используются методы и макросы, которые прдоставляют доступ к интерпретаторам из Python. А библеотека **math.h**, которая нужна для выполнения простых математических операций, используется у нас для команды fabs, которая применяется для данных типа float (команда abs в СИ для данных Python не применяется)

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

