# Calendarios ICS Aragón

**> https://github.com/abeln94/CalendariosICSAragon/releases/tag/ics <**

_Nada de este repositorio (ni scripts ni calendarios) está afiliado con el Gobierno de Aragón. El contenido aquí mostrado está generado por mí a partir de información pública disponible._

### Descripción

Este script descarga los calendarios oficiales de la página de Aragón opendata: https://opendata.aragon.es, tanto el
general común para aragón como los de las tres provincias, y genera un nuevo calendario para cada núcleo de población
con sólo los eventos generales y de dicho nucleo. Incluye todos los años disponibles.

Adicionalmente, el título y la descripción de los eventos (que tienen ambos) está intercambiado. Esto es debido a que, por defecto, el título contiene el lugar en el que es festivo (`Festivo en X`) mientras que la descripción contiene el nombre del evento (`Jueves Santo`) y se considera que es preferible que sea al contrario.

Por ejemplo: el calendario para zaragoza sólo contiene los eventos de aragón y los de zaragoza ciudad (el de opendata de
zaragoza contiene todos los eventos de todos los pueblos de la provincia de zaragoza, aparte de estar dividido por año).

Pensado para ser importado directamente en el calendario de Google (u otro servicio) a través de
url: https://github.com/abeln94/CalendariosICSAragon/releases/download/ics/zaragoza.ics ya que se actualizarán
automaticamente.

Tambien se pueden descargar si se prefiere.
