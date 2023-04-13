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
#include <Python.h>

static PyObject *py_plus(PyObject *self, PyObject *args){
  double x, y, result;

  if(!PyArg_ParseTuple(args,"dd", &x, &y))
    return NULL;
  
  result = x + y;
  
  return Py_BuildValue("d", result);
}

/* Описывает методы модуля */
static PyMethodDef ownmod_methods[] = {
{ 
    "plus",          // название функции внутри python
     py_plus,        // функция C
     METH_VARARGS,   // макрос, поясняющий, что функция у нас с аргументами
     "plus function" // документация для функции внутри python
},
{ NULL, NULL, 0, NULL } 
// так называемый sentiel. Сколько бы элементов структуры 
// у вас не было, этот нулевой элемент должен быть всегда, и при этом быть последним
};

/* Описываем наш модуль */
static PyModuleDef simple_module = {    
    PyModuleDef_HEAD_INIT,   // обязательный макрос
    "my_plus",               // my_plus.__name__
    "amazing documentation", // my_plus.__doc__
    -1,
    ownmod_methods           // сюда передаем методы модуля
};

// в названии функции обязательно должен быть префикс PyInit
PyMODINIT_FUNC PyInit_my_plus(void) {
      PyObject* m;
      // создаем модуль
      m = PyModule_Create(&simple_module);
      // если все корректно, то эта проверка не проходит
      if (m == NULL)
          return NULL;
      return m;
}


