# Module
# Модуль по дисциплине "Языки и методы программирования" для основных операций с матрицами

# Чем полезен наш модуль
Обработка реальных данных довольно часто осуществляется с помощью матриц. Большие данные удобнее всего представлять в виде массива, а его, в свою очередь, представлять в виде матрицы для дальнейших математиечских преобразований. Но именно сейчас операции с матрицами актуальны для нас как никогда. Вычислительная математика, графы, линейное программирование - всё осуществляется через матрицы. Например, в численных методах мы используем матричные операции во многих алгоритмах, каких как метод Якоби или прямой ход Гаусса. В компьютерной визуализации для 3D-графики матрицы используются для преобразования координат. Именно поэтому основные опреации с матрицами актуальны для нашего направления. Наш модуль позволяет использовать функции для основных математиечских операций с матрицами, благодаря чему пользователю не нужно самому писать код для той или иной операции - ему достаточно указать функцию и задать исходные параметры.


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
**PyObject** - обозначение типа данных из **Python.h**. **PyObject* self** - это указание на объект самого модуля, т.е. в нашем случае этот **scalar_multiplication** будет и дальше использоваться в модуле. **args** - это кортеж, состоящий из аргументов, которые передаются на вхож этой функции, в нашем случае у нас будет два аргумента - число (скаляр) **c** и матрица **listObj**. 
```C
static PyObject* scalar_multiplication(PyObject* self, PyObject* args) {
  PyObject *listObj;
  double c;
 ```
Функция **PyArg_ParseTuple** позволяет проверить, что аргументы, находящиеся в кортеже **args**, соответствуют определенному типу: "Od" означает, что **listObj** должен быть типа **O**, то есть **PyObject**, а **c** должен быть типа **d**, то есть **double**. Если в противном случае на вход мы получаем, например, два числа (**dd**), то функция выдает ошибку с сообщением **"Bad arguments !!!"**
```C 
  if( !PyArg_ParseTuple( args, "Od", &listObj, &c) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }
 ```
 Далее мы находим длину нашей матрицы. **lengthi** - количество строк в нашей матрице (или количество списков списков). Считаем длину с помощью функции **PyList_Size**. **result** - результирующая матрица, которая получится в итоге. По ходу алгоритма она будет изменяться. Очевидно, в ней столько же строк сколько в исходной матрице: мы создаем с помощью функции **PyList_New** новый список длины **lengthi**. Нужные для цикла **i,j** описываются отдельно, в отличие от Python; они будут типа **long** на случай, если пользователь задаст огромную матрицу. **lengthjpr** нужен для того, чтобы проверять правильность введенной матрицы. На каждом шаге нашего цикла мы будем длину текущей строки сравнивать с длиной предыдущей строки, чтобы вовремя обнаружить ошибку.
 
 ```C
  Py_ssize_t lengthi = PyList_Size(listObj);
  PyObject* result = PyList_New(lengthi);  
  long i,j;
  Py_ssize_t lengthjpr = -1;
 ```
 Мы передвигаемся по строкам матрицы. С помощью функции **PyList_GetItem** мы из списка **listObj** извлекаем i-ую строку и записываем в перемнную **lengthj**. Затем с помощью **PyList_Size** измеряем длину этой строки.
 
 ```C
  for(i = 0; i < lengthi; i++){    
    PyObject* tempi = PyList_GetItem(listObj, i);
    Py_ssize_t lengthj = PyList_Size(tempi);
  ```
  Далее мы проверяем, если **lengthjpr** по прежнему равняется -1, это будет означать, что на вход поступила первая строка матрицы. В этом случае мы длине предыдущей строки присваиваем ее длину (она выступает неким эталоном). А если у нас не первая строка (то есть **lengthjpr** не равняется -1), мы сравниваем, что если предыдущая длина строки не совпадает с текущей, то мы вызываем ошибку с сообщением **"Invalid matrix !!!"**
   ```C
    if( lengthjpr == -1 ) {
      lengthjpr = lengthj;
    }
    else if ( lengthjpr != lengthj ){
      PyErr_SetString(PyExc_TypeError, "Invalid matrix !!!");
      return NULL;
    }
  ```
В **row** мы записываем текущую строку новой матрицы, которую будем создавать. С помощью j перебираемся по элементам этой строки. В **tempj** мы выкладываем j-ый элемент из i-ой строки **tempi** через функцию **PyList_GetItem**. **tempj** сейчас типа **PyObject**, который понятен только для языка СИ, поэтому мы преобразовываем в "питоновский" double функцией **PyFloat_AsDouble**. Функция **PyList_SetItem** позволяет в список **row** на j-ое место положить c*elem (при этом через FromDouble мы преобразовываем в тип данных, приемлемый для СИ), где **с** - это константа, на которую мы умножаем матрицу. То есть мы идем по i-ым строкам, в которых каждый j-ый элемент умножаем на с. Получившуюся строку записываем в **result** через функцию **PyList_SetItem**, после чего возвращаем **result**.
  ```C  
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
Мы написали вспомогательную функцию, в которой различаем 1 и -1, где c = 1 - это сложение, а c = -1 - вычитание. Здесь нет  **PyObject* self**, что означает, что эта функция исключительно вспомогательная и как функция модуля использоваться не будет. На вход подается два объекта - две матрицы: **listObj1** и **listObj2**. Проверяем, что они соответствуют типу "OO" - то есть обе являются **PyObject**. 
```C
static PyObject* plusminus(PyObject* args, double c) {
  PyObject *listObj1;
  PyObject *listObj2;
  
  if( !PyArg_ParseTuple( args, "OO", &listObj1, &listObj2) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }
```
Считываем количество строк через **PyList_Size** в первой матрице **listObj1** в переменную **lengthi** и сравниваем с количеством строк во второй матрице. Если они не совпадают по размеру, это значит что сложить мы их не сможем, поэтому выдаем ошибку.
```C
  Py_ssize_t lengthi = PyList_Size(listObj1);
  if ( PyList_Size(listObj2) != lengthi ) {
      PyErr_SetString(PyExc_ValueError, "Matrix dimentions are not equal !!!");
      return NULL;
  }
```
Результирующая матрица **result** будет длины **lengthi**. Мы идем циклом по строкам матрицы. Через **PyList_GetItem** выбираем i-ую строку из каждой матрицы и записываем соответственно в **tempi1** и **tempi2**. 

```C
  PyObject* result = PyList_New(lengthi);  
  long i,j;
  Py_ssize_t lengthjpr = -1;

  for(i = 0; i < lengthi; i++){
    PyObject* tempi1 = PyList_GetItem(listObj1, i);
    PyObject* tempi2 = PyList_GetItem(listObj2, i);
    Py_ssize_t lengthj = PyList_Size(tempi1);
 ```   
 **lengthj** - длина этих строк. Выполняем примерно те же проверки, что и в предыдущей функции. Если **lengthjpr** не равен длине одной из строк матриц, то выдается ошибка с сообщением о том, какая матрица является "инвалидной".
 ```C
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
```
Как и в предыдущей функции, мы идем по столбцам, **tempj1** - j-ый элемент из **tempi1**, **tempj2**, соответственно, из **tempi2**, преобразовываем их в нужный формат и затем записываем в строку **row** сумму соответствующих элементов (если c = 1) или их разность (если с = -1)
```C
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
```
А теперь сами функции сложения и вычитания (они - **self**, так как используются в модуле). **addition** возвращает вспомогательную функцию с с = 1, то есть это сложение, а **subtraction** - с с = -1, то есть вычитание.
```C
static PyObject* addition(PyObject* self, PyObject* args) {
  return plusminus( args, 1 );
}

static PyObject* subtraction(PyObject* self, PyObject* args) {
  return plusminus( args, -1 );
}
```

### ***Векторное умножение***
Здесь мы умножаем вектор на матрицу, причем **vectorObj** будет типа **PyObject**
```C
static PyObject* vector_multiplication(PyObject* self, PyObject* args) {
  PyObject* vectorObj;
  PyObject* listObj;
  if( !PyArg_ParseTuple( args, "OO", &vectorObj, &listObj) ) {
    PyErr_SetString(PyExc_TypeError, "Bad arguments !!!");
    return NULL;
  }
```  
  **lengthi** - длина вектора, **lengthjpr** - длина строки матрицы, которую мы получаем следующим образом: вызываем сначала **PyList_GetItem** и с ее помощью выбираем нулевой элемент матрицы, то есть строку, и смотрим ее длину с помощью **PyList_Size** (то есть количество столбцов). Вектор умножается слева на матрицу, поэтому нам нужно, чтобы количество элементов из него совпадало с колиечством стобцов в матрице. Создаем **result**, который здесь будет вектором, так как при умножении вектора на матрицу именно он и получается. Выполняем проверку на размеры: если они не совпадают, "инвалидным" будет вектор либо матрица.
```C
  Py_ssize_t lengthi = PyList_Size(vectorObj);
  Py_ssize_t lengthjpr = PyList_Size(PyList_GetItem(listObj, 0));   
  PyObject* result = PyList_New(lengthjpr);  
  long i,j;  

  if ( lengthi != PyList_Size(listObj) ){
      PyErr_SetString(PyExc_TypeError, "Invalid matrix or vector !!!");
      return NULL;
  }   
 ```
 Мы передвигаемся по столбцам матрицы. **sum** - элемент, который пойдет в результирующий вектор, представляет собой сумму всех j-ых произведений i-ых элементов из вектора и соответствующего элемента из i-го столбца матрицы. Как в предыдущей функции вычисляли размер нулевой строки, так здесь вычисляем размер j-ой строки и выполняем проверку. 
 
 ```C 
  for(i = 0; i < lengthjpr; i++){
    double sum = 0;
    for (j = 0; j < lengthi; j++){
       Py_ssize_t lengthj = PyList_Size(PyList_GetItem(listObj, j));
       if ( lengthjpr != lengthj ){
          PyErr_SetString(PyExc_TypeError, "Invalid matrix !!!");
          return NULL;
       }      
 ```
 Берем j-ый элемент из вектора и записываем в **elemv**, а в матрице выбираем j-ый элемент из i-ого столбца и записываем в **tempi**, после чего преобразовываем в нужный тип в **elemm**. В **sum** мы складываем все соответствующие **elemv** и **elemm**. Получившийся **sum** записываем в **result**
  ```C 
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
