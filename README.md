# Module
# Модуль по дисциплине "Языки и методы программирования" для основных операций с матрицами

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

### ***Сложение и вычитание матриц***

```C
static PyObject* plusminus(PyObject* args, double c) {
  PyObject *listObj1;
  PyObject *listObj2;
  
  if( !PyArg_ParseTuple( args, "OO", &listObj1, &listObj2) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }

  Py_ssize_t lengthi = PyList_Size(listObj1);
  if ( PyList_Size(listObj2) != lengthi ) {
      PyErr_SetString(PyExc_ValueError, "Matrix dimentions are not equal !!!");
      return NULL;
  }

  PyObject* result = PyList_New(lengthi);  
  long i,j;
  Py_ssize_t lengthjpr = -1;

  for(i = 0; i < lengthi; i++){
    PyObject* tempi1 = PyList_GetItem(listObj1, i);
    PyObject* tempi2 = PyList_GetItem(listObj2, i);
    Py_ssize_t lengthj = PyList_Size(tempi1);
    if( lengthjpr == -1 ) {
      lengthjpr = lengthj;
    }
    else if ( lengthjpr != lengthj ){
      PyErr_SetString(PyExc_TypeError, "Invalid matrix 1 !!!");
      return NULL;
    }

    if ( lengthjpr != PyList_Size(tempi2) ){
      PyErr_SetString(PyExc_TypeError, "Invalid matrix 2 !!!");
      return NULL;
    }

    PyObject* row = PyList_New(lengthj);
    for (j = 0; j <lengthj; j++){
       PyObject* tempj1 = PyList_GetItem(tempi1, j);
       PyObject* tempj2 = PyList_GetItem(tempi2, j);
       double elem1 = PyFloat_AsDouble(tempj1);
       double elem2 = PyFloat_AsDouble(tempj2);
       PyList_SetItem(row, j, PyFloat_FromDouble(elem1+c*elem2)); 
    }
    PyList_SetItem(result, i, row);    
  }  
  
  return result;
}


static PyObject* addition(PyObject* self, PyObject* args) {
  return plusminus( args, 1 );
}

static PyObject* subtraction(PyObject* self, PyObject* args) {
  return plusminus( args, -1 );
}
```

### ***Векторное умножение***

```C
static PyObject* vector_multiplication(PyObject* self, PyObject* args) {
  PyObject* vectorObj;
  PyObject* listObj;
  if( !PyArg_ParseTuple( args, "OO", &vectorObj, &listObj) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }

  Py_ssize_t lengthi = PyList_Size(vectorObj);
  Py_ssize_t lengthjpr = PyList_Size(PyList_GetItem(listObj, 0));   
  PyObject* result = PyList_New(lengthjpr);  
  long i,j;  

  if ( lengthi != PyList_Size(listObj) ){
      PyErr_SetString(PyExc_TypeError, "Invalid matrix or vector !!!");
      return NULL;
  }   
  
  for(i = 0; i < lengthjpr; i++){
    double sum = 0;
    for (j = 0; j < lengthi; j++){
       Py_ssize_t lengthj = PyList_Size(PyList_GetItem(listObj, j));
       if ( lengthjpr != lengthj ){
          PyErr_SetString(PyExc_TypeError, "Invalid matrix !!!");
          return NULL;
       }      
 
       double elemv = PyFloat_AsDouble(PyList_GetItem(vectorObj, j));
       PyObject* tempi = PyList_GetItem(PyList_GetItem(listObj, j), i);
       double elemm = PyFloat_AsDouble(tempi);
       sum += elemv * elemm;        
    }        
   
    PyList_SetItem(result, i, PyFloat_FromDouble(sum));       
  }  
  
  return result;
}
```

### ***Транспонирование***

```C

static PyObject* transposition(PyObject* self, PyObject* args) {
  PyObject *listObj;  
  if( !PyArg_ParseTuple( args, "O", &listObj) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }

  Py_ssize_t lengthi = PyList_Size(listObj);
  PyObject* result = PyList_New(PyList_Size(PyList_GetItem(listObj, 0)));  
  long i,j;
  Py_ssize_t lengthjpr = -1;

  for(i = 0; i < PyList_Size(result); i++){   
    PyObject* row = PyList_New(lengthi);
    for (j = 0; j <lengthi; j++){
       PyObject* tempj = PyList_GetItem(listObj, j);    
       Py_ssize_t lengthj = PyList_Size(tempj);
       if( lengthjpr == -1 ) {
          lengthjpr = lengthj;
       }
       else if ( lengthjpr != lengthj ){
          PyErr_SetString(PyExc_TypeError, "Invalid matrix !!!");
          return NULL;
       }
       PyObject* temp = PyList_GetItem(PyList_GetItem(listObj, j), i);
       double elem = PyFloat_AsDouble(temp);
       PyList_SetItem(row, j, PyFloat_FromDouble(elem)); 
    }
    PyList_SetItem(result, i, row);    
  }  
  
  return result;
}
```

### ***Определитель***

```C

static PyObject* determinant(PyObject* self, PyObject* args) {
  PyObject *listObj; 
  if( !PyArg_ParseTuple( args, "O", &listObj) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }

  Py_ssize_t lengthi = PyList_Size(listObj);
  Py_ssize_t lengthj = PyList_Size(PyList_GetItem(listObj, 0));
  if ( lengthi != lengthj ) {
     PyErr_SetString(PyExc_TypeError, "Not a square matrix !!!");
     return NULL;
  }

  PyObject* a = PyList_New(lengthi);
  long i,j,k;
  
  for( i=0; i<lengthi; i++ ) {
    PyObject* row = PyList_GetItem(listObj, i);
    if( PyList_Size(row) != lengthi ) {
      PyErr_SetString(PyExc_ValueError, "Invalid matrix !!!");
      return NULL;
    }

    PyObject* r = PyList_New(lengthi);
    for( j=0; j<lengthi; j++ ) 
      PyList_SetItem(r, j, PyList_GetItem(row, j));

    PyList_SetItem(a, i, r);
  }

  double temp1, temp2, temp3, det = 1;
  const double EPS = 1E-9;
  
  for( i=0; i<lengthi; i++ ) {
    k = i;

    for( j=i+1; j<lengthi; j++ ) {
      temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, j), i) );
      temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, k), i) );
      if( fabs(temp1) > fabs(temp2) ) k = j;
    }

    temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, k), i) );
    if( fabs(temp1) < EPS ) {
	det = 0;
	break;
    }

    if( i != k ) {
      det = -det;
      for( j=0; j<lengthi; j++ ) {
        temp1 = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(a, i), j));
	temp2 = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(a, k), j));
        PyList_SetItem(PyList_GetItem(a, i), j, PyFloat_FromDouble(temp2));
        PyList_SetItem(PyList_GetItem(a, k), j, PyFloat_FromDouble(temp1));
      }
    }

    temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, i), i) );
    det *= temp1;

    for( j=i+1; j<lengthi; j++ ) {
       temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, i), j) );
       PyList_SetItem( PyList_GetItem(a, i), j, PyFloat_FromDouble(temp2/temp1) ); 
    }

    for( j=0; j<lengthi; j++ ) {
      temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, j), i) );
      if( (j != i) && (fabs(temp1) > EPS) ) {
	 for( k=i+1; k<lengthi; k++ ) {
	   temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, i), k) );
           temp3 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, j), k) );
           PyList_SetItem( PyList_GetItem(a, j), k, PyFloat_FromDouble(temp3-temp2*temp1) );
         }
      }
    }
  }

  return PyFloat_FromDouble(det);
}
```


### ***Умножение матриц***

```C

static PyObject* matrix_multiplication(PyObject* self, PyObject* args) {
  PyObject *listObj1;
  PyObject *listObj2;  
  if( !PyArg_ParseTuple( args, "OO", &listObj1, &listObj2) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }

  Py_ssize_t lengthst = PyList_Size(PyList_GetItem(listObj1, 0));
  Py_ssize_t lengthsr = PyList_Size(listObj2);
  if ( lengthst != lengthsr ){
     PyErr_SetString(PyExc_ValueError, "Not suitable matrixs for multiplication !!!");
     return NULL;
  }  

  Py_ssize_t lengthjpr = PyList_Size(PyList_GetItem(listObj2, 0));
  Py_ssize_t lengthi = PyList_Size(listObj1);
  PyObject* result = PyList_New(lengthi);  
  long i,j,k;

  for(i = 0; i < lengthst; i++) {
    if( PyList_Size(PyList_GetItem(listObj2, i)) != lengthjpr ) {
      PyErr_SetString(PyExc_TypeError, "Invalid matrix 2 !!!");
      return NULL;
    }
  }
    
  for(i = 0; i < lengthi; i++){ 
    if( PyList_Size(PyList_GetItem(listObj1, i)) != lengthst ) {
      PyErr_SetString(PyExc_TypeError, "Invalid matrix 1 !!!");
      return NULL;
    }
       
    PyObject* row = PyList_New(lengthjpr);     
    for (j = 0; j < lengthjpr; j++){
       double sum = 0;     
       for (k=0; k < lengthst; k++){
           PyObject* temp1 = PyList_GetItem(PyList_GetItem(listObj1, i), k);
           PyObject* temp2 = PyList_GetItem(PyList_GetItem(listObj2, k), j);
           double elem1 = PyFloat_AsDouble(temp1);
           double elem2 = PyFloat_AsDouble(temp2);
           sum += elem1*elem2;
       }

       PyList_SetItem(row, j, PyFloat_FromDouble(sum));       
    }        
   
    PyList_SetItem(result, i, row);       
  }  
  
  return result;
}
```

### ***Обратная матрица***

```C

static PyObject* inversion(PyObject* self, PyObject* args) {
  PyObject *listObj; 
  if( !PyArg_ParseTuple( args, "O", &listObj) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }

  Py_ssize_t lengthi = PyList_Size(listObj);
  Py_ssize_t lengthj = PyList_Size(PyList_GetItem(listObj, 0));
  if ( lengthi != lengthj ) {
     PyErr_SetString(PyExc_TypeError, "Not a square matrix !!!");
     return NULL;
  }

  const double EPS = 1E-9;
  double det = 1;
  
  PyObject* a = PyList_New(lengthi);
  long i,j,k;
  
  for( i=0; i<lengthi; i++ ) {
    PyObject* row = PyList_GetItem(listObj, i);
    if( PyList_Size(row) != lengthi ) {
      PyErr_SetString(PyExc_ValueError, "Invalid matrix !!!");
      return NULL;
    }

    PyObject* r = PyList_New(lengthi);
    for( j=0; j<lengthi; j++ ) 
      PyList_SetItem(r, j, PyList_GetItem(row, j));

    PyList_SetItem(a, i, r);
  }


  PyObject* e = PyList_New(lengthi);
  for( i=0; i<lengthi; i++ ) {
     PyObject* r = PyList_New(lengthi);
     for( j=0; j<lengthi; j++ ) 
       if( i == j ) {
          PyList_SetItem(r, j, PyFloat_FromDouble(1));
       } else {
          PyList_SetItem(r, j, PyFloat_FromDouble(0));
       }
     PyList_SetItem(e, i, r);
  }


  double temp1, temp2, temp3;

  for( i=0; i<lengthi; i++ ) {
    k = i;

    for( j=i+1; j<lengthi; j++ ) {
      temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, j), i) );
      temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, k), i) );
      if( fabs(temp1) > fabs(temp2) ) k = j;
    }

    temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, k), i) );
    if( fabs(temp1) < EPS ) {
      PyErr_SetString(PyExc_ValueError, "Determinant = 0 !!!");
      return NULL;
    }

    if( i != k ) {
      det = -det;
      for( j=0; j<lengthi; j++ ) {
        temp1 = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(a, i), j));
	temp2 = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(a, k), j));
        PyList_SetItem(PyList_GetItem(a, i), j, PyFloat_FromDouble(temp2));
        PyList_SetItem(PyList_GetItem(a, k), j, PyFloat_FromDouble(temp1));

        temp1 = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(e, i), j));
	temp2 = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(e, k), j));
        PyList_SetItem(PyList_GetItem(e, i), j, PyFloat_FromDouble(temp2));
        PyList_SetItem(PyList_GetItem(e, k), j, PyFloat_FromDouble(temp1));
      }
    }

    temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, i), i) );
    det *= temp1;

    for( j=i; j<lengthi; j++ ) {
       temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, i), j) );
       PyList_SetItem( PyList_GetItem(a, i), j, PyFloat_FromDouble(temp2/temp1) ); 
    }

    for( j=0; j<lengthi; j++ ) {
       temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(e, i), j) );
       PyList_SetItem( PyList_GetItem(e, i), j, PyFloat_FromDouble(temp2/temp1) ); 
    }

    for( j=i+1; j<lengthi; j++ ) {
      temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, j), i) );
      if( fabs(temp1) > EPS ) {
	 for( k=0; k<lengthi; k++ ) {
	   temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, i), k) );
           temp3 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, j), k) );
           PyList_SetItem( PyList_GetItem(a, j), k, PyFloat_FromDouble(temp3-temp2*temp1) );

	   temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(e, i), k) );
           temp3 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(e, j), k) );
           PyList_SetItem( PyList_GetItem(e, j), k, PyFloat_FromDouble(temp3-temp2*temp1) );
         }
      }
    }
  }

  for(i = lengthi-1; i > 0; i--) {
     for(int k = 0; k < i; k++) {
        temp1 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, k), i) );
        if (fabs(temp1) > EPS) {
              for (j = i-1; j < lengthi; j++) {
	         temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, i), j) );
                 temp3 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(a, k), j) );
                 PyList_SetItem( PyList_GetItem(a, k), j, PyFloat_FromDouble(temp3-temp2*temp1) );
              }

              for (int j = 0; j < lengthi; j++){
	         temp2 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(e, i), j) );
                 temp3 = PyFloat_AsDouble( PyList_GetItem(PyList_GetItem(e, k), j) );
                 PyList_SetItem( PyList_GetItem(e, k), j, PyFloat_FromDouble(temp3-temp2*temp1) );
              }
        }
     }
  }


   return e;
}
```
