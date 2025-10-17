from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton, MDIconButton
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivy.uix.checkbox import CheckBox
from kivymd.uix.textfield import *
from kivymd.uix.dialog import MDDialog

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.boxlayout import MDBoxLayout

# from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


from isdb import DataBase
import pandas as pd

from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.list import IconLeftWidget



class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class Ingresos(Screen):
    bd = DataBase()
    # Crea la BD
    # try:
    #     bd.crearBD()
    #     bd.crearTabla_movimientos()
    #     bd.crearTabla_categorias()
    #     bd.insertar_categorias()
    # except Exception as e:
    #     pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Toolbar
        self.toolbar = MDTopAppBar(title="Mis Finanzas")
        self.toolbar.pos_hint = {"top": 1}

        self.label1 = MDLabel(
            text="Registrar Movimiento!",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
        )

        self.add_widget(self.toolbar)
        self.add_widget(self.label1)

        # Botón para agregar ingreso
        self.boton_agregar = MDFillRoundFlatButton(text="Registrar Movimiento", icon="check", md_bg_color="purple", text_color="yellow", pos_hint={"center_x": 0.5, "center_y": 0.1}, on_press= lambda x: self.press_btn_guardar_ingreso())
        self.add_widget(self.boton_agregar)

        # Layout para mostrar ingresos
        # self.lista = StackLayout(size_hint=(1, None), spacing='5dp', padding='10dp')

        # for i in range(5):  # Simulando 10 ingresos
        #     self.lista.add_widget(MDRaisedButton(text=f"Ingreso {i+1}", size_hint=(None, None), size=('200dp', '40dp')))
        # self.lista.bind(minimum_height=self.lista.setter('height'))

        # self.scroll = ScrollView()
        # self.scroll.add_widget(self.lista)
        # self.add_widget(self.scroll)        

        # checkbox
        # self.cbx = CheckBox(active=True, size_hint=(None, None), size=('48dp', '48dp'), pos_hint={"center_x": 0.5, "center_y": 0.2})
        # self.cbx.bind(active=self.cbx_active)
        # self.add_widget(self.cbx)

        # self.label1 = MDLabel(
        #     text="Enviar correo", halign="center", theme_text_color="Custom", text_color=(1, 1, 1, 1), font_style="H6", pos_hint={"center_x": 0.5, "center_y": 0.3})
        # self.add_widget(self.label1)

        # === Formulario ===

        # === Dropdown Categorías ===
        self.txt_tipo_movimiento = MDTextField(
            hint_text="Selecciona Tipo Movimiento",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            size_hint_x=None,
            width="200dp",
        )
        self.add_widget(self.txt_tipo_movimiento)

        tipo_movimientos = ['Ingreso', 'Egreso']
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "wallet",  # Puedes personalizar íconos aquí
                "height": dp(56),
                "text": f"{movimiento}",
                "on_release": lambda x=f"{movimiento}": self.set_tipo_movimiento(x),
            }
            for movimiento in tipo_movimientos
        ]

        self.menu_categorias_movimientos = MDDropdownMenu(
            caller=self.txt_tipo_movimiento,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )

        # Abrir el menú al enfocar el campo
        self.txt_tipo_movimiento.bind(focus=lambda instance, value: self.menu_categorias_movimientos.open() if value else None)


        # Cuadro de texto
        self.txt_monto = MDTextField(hint_text="Monto", helper_text = 'Ingrese el monto', helper_text_mode = 'on_focus', pos_hint={"center_x": 0.5, "center_y": 0.6}, size_hint_x=None, width="200dp", on_text_validate = lambda x: self.validate_fecha())
        self.add_widget(self.txt_monto)

        self.txt_descripcion = MDTextField(hint_text="Descripcion", helper_text = 'Ingrese el monto', helper_text_mode = 'on_focus', pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint_x=None, width="200dp", on_text_validate = lambda x: self.validate_fecha())
        self.add_widget(self.txt_descripcion)

        # === Seccion Fecha ===
        self.txt_fecha = MDTextField(
            hint_text="Selecciona una fecha",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            size_hint_x=None,
            width="200dp"
        )
        self.txt_fecha.bind(focus=self.on_fecha_focus)
        self.add_widget(self.txt_fecha)
        # === Fin Seccion Fecha ===

        # self.txt_fecha = MDTextField(hint_text="Fecha", helper_text = 'Ingrese la fecha', helper_text_mode = 'on_focus', pos_hint={"center_x": 0.5, "center_y": 0.4}, size_hint_x=None, width="200dp", on_text_validate = lambda x: self.validate_fecha())
        # self.add_widget(self.txt_fecha)

        # === Dropdown Categorías ===
        self.txt_categoria = MDTextField(
            hint_text="Selecciona Categoría",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            size_hint_x=None,
            width="200dp",
        )
        self.add_widget(self.txt_categoria)

        # categorias = ['Sueldo', 'Comida', 'Transporte', 'Renta', 'Entretenimiento', 'Ahorros']
        categorias = self.bd.obtener_categorias_activas()
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "wallet",  # Puedes personalizar íconos aquí
                "height": dp(56),
                "text": f"{categoria}",
                "on_release": lambda x=f"{categoria}": self.set_categoria(x),
            }
            for categoria in categorias
        ]

        self.menu_categorias = MDDropdownMenu(
            caller=self.txt_categoria,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )

        # Abrir el menú al enfocar el campo
        # self.txt_categoria.bind(focus=lambda instance, value: self.menu_categorias.open() if value else None)
        self.txt_categoria.bind(focus=self.on_focus_categoria)        
        # === Fin del Formulario ===
        # Cambiar de pantalla -> Categorias
        self.btn_cambiar_pantalla = MDRaisedButton(text="Ir a Categorias", pos_hint={"center_x": 0.9, "center_y": 0.1}, on_press=lambda x: self.ir_a_egresos())

        self.add_widget(self.btn_cambiar_pantalla)

        # Cambiar de pantalla -> Resumen
        self.btn_cambiar_pantalla_resumen = MDRaisedButton(text="INICIO", pos_hint={"center_x": 0.1, "center_y": 0.1}, on_press=lambda x: self.ir_a_inicio())

        self.add_widget(self.btn_cambiar_pantalla_resumen)

        # # bOTON SALIR
        # self.boton_salir = MDFillRoundFlatButton(text="Salir", icon="exit-to-app", md_bg_color="red", text_color="white", pos_hint={"center_x": 0.1, "center_y": 0.1}, on_press=lambda x: self.salir())
        # self.add_widget(self.boton_salir)

    def press_btn_guardar_ingreso(self):
        tipo_movimiento = self.txt_tipo_movimiento.text
        categoria_id = self.bd.selecciona_categoria_id(self.txt_categoria.text)
        monto = self.txt_monto.text
        descripcion = self.txt_descripcion.text
        fecha = self.txt_fecha.text

        print(f'tipo_movimiento: {tipo_movimiento}')
        print(f'monto: {monto}')
        print(f'descripcion: {descripcion}')
        print(f'fecha: {fecha}')
        print(f'categoria id: {categoria_id}')

        self.bd.agregar_movimiento(tipo_movimiento.lower(), monto, descripcion, fecha, categoria_id)

        self.txt_tipo_movimiento.text = ""
        self.txt_categoria.text = ""
        self.txt_monto.text = ""
        self.txt_descripcion.text = ""
        self.txt_fecha.text = ""

        # Mostrar diálogo de confirmación
        self.dialogo_confirmacion = MDDialog(
            title="¡Movimiento agregado!",
            text="Se agregó un nuevo movimiento.",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_press=lambda x: self.dialogo_confirmacion.dismiss()
                )
            ]
        )
        self.dialogo_confirmacion.open()

    def ir_a_egresos(self):
        self.manager.transition.direction = "left"
        self.manager.current = "categorias"
    
    def ir_a_inicio(self):
        self.manager.transition.direction = "right"
        self.manager.current = "inicio"

    def cbx_active(self, checkbox, value):
        if value:
            print("Checkbox activo")
        else:
            print("Checkbox inactivo")
    
    def validate_fecha(self):
        fecha = self.txt_fecha.text
        print(f"Fecha ingresada: {fecha}")
        # Aquí se puede agregar lógica para validar el formato de la fecha

    def salir(self):
        self.dialog_salir = MDDialog(
            title="Está seguro de que quiere salir de la apliacion",
            buttons=[
                MDRaisedButton(text="Si", on_press=lambda x: quit()), MDRaisedButton(text="No", on_press=lambda x: self.dialog_salir.dismiss())
            ])
        self.dialog_salir.open()

    def set_categoria(self, categoria):
        self.txt_categoria.text = categoria
        self.menu_categorias.dismiss()

    def set_tipo_movimiento(self, movimiento):
        self.txt_tipo_movimiento.text = movimiento
        self.menu_categorias_movimientos.dismiss()

    def on_fecha_focus(self, instance, value):
        if value:  # Solo cuando se enfoca
            date_picker = MDDatePicker()
            date_picker.bind(on_save=self.on_fecha_save)
            date_picker.open()

    def on_fecha_save(self, instance, value, date_range):
        self.txt_fecha.text = str(value)

    def actualizar_menu_categorias(self):
        categorias = self.bd.obtener_categorias_activas()

        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "wallet",
                "height": dp(56),
                "text": f"{categoria}",
                "on_release": lambda x=f"{categoria}": self.set_categoria(x),
            }
            for categoria in categorias
        ]

        # Cerrar menú actual si existe
        if hasattr(self, 'menu_categorias'):
            self.menu_categorias.dismiss()

        # Crear nuevo menú
        self.menu_categorias = MDDropdownMenu(
            caller=self.txt_categoria,
            items=menu_items,
            position="auto",
            width_mult=4,
        )

        self.menu_categorias.open()
    
    def on_focus_categoria(self, instance, value):
        if value:  # Solo si se enfoca
            self.actualizar_menu_categorias()
    
    # def on_enter(self):
    #     self.actualizar_menu_categorias()

class Categorias(Screen):
    bd = DataBase()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Toolbar
        self.toolbar = MDTopAppBar(title="Mis Finanzas")
        self.toolbar.pos_hint = {"top": 1}

        self.label1 = MDLabel(
            text="Categorias!",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )

        self.add_widget(self.toolbar)
        self.add_widget(self.label1)

        self.btn_cambiar_pantalla = MDRaisedButton(text="Ir a Movimientos", pos_hint={"center_x": 0.9, "center_y": 0.1}, on_press=lambda x: self.ir_a_ingresos())

        self.add_widget(self.btn_cambiar_pantalla)

        # agregar categoria
        # Cuadro de texto
        self.txt_nueva_categoria = MDTextField(hint_text="Agregar Categoria", helper_text = 'Ingrese nueva Categoria', helper_text_mode = 'on_focus', pos_hint={"center_x": 0.5, "center_y": 0.8}, size_hint_x=None, width="200dp", on_text_validate = lambda x: self.validate_fecha())
        self.add_widget(self.txt_nueva_categoria)

        self.btn_agregar_categoria = MDRaisedButton(text="Agregar Categoria", pos_hint={"center_x": 0.8, "center_y": 0.8}, on_press=lambda x: self.agregar_categoria())
        self.add_widget(self.btn_agregar_categoria)

        # Sección: CATEGORIAS
        # === Lista de Categorías ===
        self.scroll = ScrollView(pos_hint={"center_x": 0.5, "center_y": 0.4}, size_hint=(1, 0.5))
        self.lista = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing="10dp", padding="10dp")
        self.lista.bind(minimum_height=self.lista.setter("height"))
        self.scroll.add_widget(self.lista)
        self.add_widget(self.scroll)

        # Cargar categorías desde la base de datos
        self.cargar_categorias()
       

    def ir_a_ingresos(self):
        self.manager.transition.direction = "right"
        self.manager.current = "ingresos"
    
    def agregar_categoria(self):
        nombre = self.txt_nueva_categoria.text.strip()
        if nombre:
            resultado = self.bd.agregar_categoria(nombre)  # Asegúrate de tener este método
            self.txt_nueva_categoria.text = ''
            self.cargar_categorias()
    
    def cargar_categorias(self):
        """Carga las categorías activas desde la base de datos y las muestra en la interfaz."""
        self.lista.clear_widgets()
        categorias = self.bd.obtener_categorias_activas()
        for categoria in categorias:
            fila = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="40dp",
                spacing="10dp"
            )

            label = MDLabel(
                text=categoria,
                halign="left",
                size_hint_x=0.85
            )

            btn_eliminar = MDIconButton(
                icon="delete",
                theme_text_color="Custom",
                text_color=(1, 0, 0, 1),
                on_release=lambda x, c=categoria: self.eliminar_categoria(c)
            )

            fila.add_widget(label)
            fila.add_widget(btn_eliminar)
            self.lista.add_widget(fila)

    def eliminar_categoria(self, nombre):
        self.bd.desactivar_categoria(nombre)  # Asegúrate de tener este método
        self.cargar_categorias()

class Inicio(Screen):
    bd = DataBase()

    try:
        bd.crearBD()
        bd.crearTabla_movimientos()
        bd.crearTabla_categorias()
        bd.insertar_categorias()
    except Exception as e:
        pass
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Toolbar
        self.toolbar = MDTopAppBar(title="Mis Finanzas")
        self.toolbar.pos_hint = {"top": 1}

        self.label1 = MDLabel(
            text="Mis Movimientos!",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )

        self.add_widget(self.toolbar)
        self.add_widget(self.label1)

        total_ingresos = self.bd.calcular_movimiento('ingreso')
        if total_ingresos:
            total_ingresos
        else:
            total_ingresos= 0

        total_egresos = self.bd.calcular_movimiento('egreso')
        if total_egresos:
            total_ingresos
        else:
            total_egresos= 0

        saldo_dispnible = total_ingresos - total_egresos
        # Dsiponible
        self.label2 = MDLabel(
            text="Disponible: " +str(round(saldo_dispnible,2)),
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            pos_hint={"center_x": 0.15, "center_y": 0.8},
        )
        self.add_widget(self.label2)

        # Ingresos
        self.label3 = MDLabel(
            text="Ingresos: " + str(round(total_ingresos,2)),
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
        )
        self.add_widget(self.label3)

        # Egresos
        self.label4 = MDLabel(
            text="Egresos: " + str(round(total_egresos,2)),
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            pos_hint={"center_x": 0.85, "center_y": 0.8},
        )
        self.add_widget(self.label4)

        # === Seccion Fecha ===
        self.txt_fecha_inicio = MDTextField(
            hint_text="Selecciona Fecha Inicio",
            pos_hint={"center_x": 0.15, "center_y": 0.6},
            size_hint_x=None,
            width="200dp"
        )
        self.txt_fecha_inicio.bind(focus=self.on_fecha_focus)
        self.add_widget(self.txt_fecha_inicio)

        self.txt_fecha_fin = MDTextField(
            hint_text="Selecciona Fecha Fin",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            size_hint_x=None,
            width="200dp"
        )
        self.txt_fecha_fin.bind(focus=self.on_fecha_focus_fin)
        self.add_widget(self.txt_fecha_fin)

        self.btn_ver_movimientos = MDRaisedButton(text="Ver Movimientos", pos_hint={"center_x": 0.85, "center_y": 0.6}, on_press=lambda x: self.ver_movimientos())

        self.add_widget(self.btn_ver_movimientos)
        # === Fin Seccion Fecha ===

        # === Aqui se debe cargar el dataframe
        self.df = self.bd.generar_tabla_movimiento()
        if self.df.empty:
            self.df = pd.DataFrame(columns=["Fecha", "Categoria", "Tipo Movimiento", "Descripcion", "Monto"])
        # # Crear tabla desde el DataFrame
        # table_layout = GridLayout(cols=len(self.df.columns), size_hint_y=None)
        # table_layout.bind(minimum_height=table_layout.setter('height'))

        # # Encabezados
        # for col in self.df.columns:
        #     table_layout.add_widget(Label(
        #         text=str(col),
        #         size_hint_y=None,
        #         height=40,
        #         bold=True
        #     ))

        # # Filas
        # for i in range(len(self.df)):
        #     for col in self.df.columns:
        #         table_layout.add_widget(Label(
        #             text=str(self.df.iloc[i][col]),
        #             size_hint_y=None,
        #             height=30
        #         ))

        # # Scroll para la tabla
        # scroll_view = ScrollView(size_hint=(1, 0.3), pos_hint={"center_x": 0.5, "center_y": 0.4})
        # scroll_view.add_widget(table_layout)
        # self.add_widget(scroll_view)

        self.mostrar_tabla()
        # === Fin tabla movimientos

        self.btn_cambiar_pantalla = MDRaisedButton(text="Ir a Movimientos", pos_hint={"center_x": 0.9, "center_y": 0.1}, on_press=lambda x: self.ir_a_ingresos())

        self.add_widget(self.btn_cambiar_pantalla)

        # bOTON SALIR
        self.boton_salir = MDFillRoundFlatButton(text="Salir", icon="exit-to-app", md_bg_color="red", text_color="white", pos_hint={"center_x": 0.1, "center_y": 0.1}, on_press=lambda x: self.salir())
        self.add_widget(self.boton_salir)

    def ir_a_ingresos(self):
        self.manager.transition.direction = "left"
        self.manager.current = "ingresos"
    
    def ver_movimientos(self):
        # Obtener fechas del usuario
        fecha_inicio = self.txt_fecha_inicio.text
        fecha_fin = self.txt_fecha_fin.text

        # Obtener nuevos datos desde la base de datos
        self.df = self.bd.generar_tabla_movimiento(fecha_inicio, fecha_fin)
        if self.df.empty:
            self.df = pd.DataFrame(columns=["Fecha", "Categoria", "Tipo Movimiento", "Descripcion", "Monto"])

        # Calcular nuevos totales
        if self.df.empty:
            ingresos_df, egresos_df = 0, 0
        else:
                ingresos_df = self.df[self.df['Tipo Movimiento'] == 'ingreso']
                egresos_df = self.df[self.df['Tipo Movimiento'] == 'egreso']

        total_ingresos = ingresos_df['Monto'].sum()
        total_egresos = egresos_df['Monto'].sum()
        saldo_disponible = total_ingresos - total_egresos

        # Actualizar etiquetas
        self.label2.text = f"Disponible: {round(saldo_disponible,2)}"
        self.label3.text = f"Ingresos: {round(total_ingresos,2)}"
        self.label4.text = f"Egresos: {round(total_egresos,2)}"

        # Eliminar tabla anterior si existe
        if hasattr(self, 'scroll_view'):
            self.remove_widget(self.scroll_view)

        # Mostrar tabla actualizada
        self.mostrar_tabla()
    
    def mostrar_tabla(self):
        # Crear tabla desde el DataFrame actualizado
        table_layout = GridLayout(cols=len(self.df.columns), size_hint_y=None)
        table_layout.bind(minimum_height=table_layout.setter('height'))

        # Encabezados
        for col in self.df.columns:
            table_layout.add_widget(Label(
                text=str(col),
                size_hint_y=None,
                height=40,
                bold=True
            ))

        # Filas
        for i in range(len(self.df)):
            for col in self.df.columns:
                table_layout.add_widget(Label(
                    text=str(self.df.iloc[i][col]),
                    size_hint_y=None,
                    height=30
                ))

        # Scroll para la tabla (se guarda como atributo para eliminar luego)
        self.scroll_view = ScrollView(size_hint=(1, 0.3), pos_hint={"center_x": 0.5, "center_y": 0.4})
        self.scroll_view.add_widget(table_layout)
        self.add_widget(self.scroll_view)

    def on_fecha_focus(self, instance, value):
        if value:  # Solo cuando se enfoca
            date_picker = MDDatePicker()
            date_picker.bind(on_save=self.on_fecha_save)
            date_picker.open()
    
    def on_fecha_save(self, instance, value, date_range):
        self.txt_fecha_inicio.text = str(value)

    def on_fecha_focus_fin(self, instance, value):
        if value:  # Solo cuando se enfoca
            date_picker = MDDatePicker()
            date_picker.bind(on_save=self.on_fecha_save_fin)
            date_picker.open()
    
    def on_fecha_save_fin(self, instance, value, date_range):
        self.txt_fecha_fin.text = str(value)

    def salir(self):
        self.dialog_salir = MDDialog(
            title="Está seguro de que quiere salir de la apliacion",
            buttons=[
                MDRaisedButton(text="Si", on_press=lambda x: quit()), MDRaisedButton(text="No", on_press=lambda x: self.dialog_salir.dismiss())
            ])
        self.dialog_salir.open()



# Administrador de pantallas
class MisApp(MDApp):
    def build(self):
        SC = ScreenManager()
        SC.add_widget(Inicio(name="inicio"))
        SC.add_widget(Ingresos(name="ingresos"))
        SC.add_widget(Categorias(name="categorias"))

        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Dark"

        return SC


MisApp().run()