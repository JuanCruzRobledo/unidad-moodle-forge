# -*- coding: utf-8 -*-
"""
Convierte un YAML simple de preguntas de opcion multiple al formato Moodle XML
importable (ver references/formato-preguntas-moodle-xml.md para el detalle del
schema y la convencion de codigos).

YAML de entrada esperado:

    categoria: "Unidad 1 - Fundamentos Spring Boot/Actividad 1"
    preguntas:
      - codigo: "SPRING 1"
        enunciado: "<p>Que anotacion define un bean gestionado por Spring?</p>"
        feedback_general: "<p>@Component y sus especializaciones registran beans.</p>"
        puntaje: 1.0
        opciones:
          - texto: "<code>@Component</code>"
            correcta: true
            feedback: "Correcto."
          - texto: "<code>@Import</code>"
            correcta: false
            feedback: "Incorrecto, esa anotacion importa configuraciones."

Uso:
    python generar_pregunta_xml.py --entrada preguntas-actividad-1.yml \
        --salida preguntas-actividad-1.xml
"""
import argparse
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

import yaml


def _cdata_text(parent_tag: str, contenido: str, formato: str = "html") -> ET.Element:
    el = ET.Element(parent_tag, format=formato)
    text_el = ET.SubElement(el, "text")
    text_el.text = contenido
    return el


def construir_pregunta(pregunta: dict) -> ET.Element:
    opciones = pregunta["opciones"]
    correctas = [o for o in opciones if o.get("correcta")]
    if len(correctas) != 1:
        raise ValueError(f"La pregunta '{pregunta.get('codigo')}' debe tener exactamente 1 opcion correcta, tiene {len(correctas)}")

    q = ET.Element("question", type="multichoice")
    q.append(_nombre(pregunta["codigo"]))
    q.append(_cdata_text("questiontext", pregunta["enunciado"]))
    if pregunta.get("feedback_general"):
        q.append(_cdata_text("generalfeedback", pregunta["feedback_general"]))

    puntaje = pregunta.get("puntaje", 1.0)
    ET.SubElement(q, "defaultgrade").text = f"{puntaje:.7f}"
    ET.SubElement(q, "penalty").text = "0.3333333"
    ET.SubElement(q, "hidden").text = "0"
    ET.SubElement(q, "single").text = "true"
    ET.SubElement(q, "shuffleanswers").text = "true"
    ET.SubElement(q, "answernumbering").text = "abc"

    for op in opciones:
        fraction = "100" if op.get("correcta") else "0"
        answer = ET.Element("answer", fraction=fraction, format="html")
        text_el = ET.SubElement(answer, "text")
        text_el.text = op["texto"]
        if op.get("feedback"):
            fb = ET.SubElement(answer, "feedback", format="html")
            ET.SubElement(fb, "text").text = op["feedback"]
        q.append(answer)

    return q


def _nombre(codigo: str) -> ET.Element:
    name = ET.Element("name")
    text_el = ET.SubElement(name, "text")
    text_el.text = codigo
    return name


def construir_categoria(categoria: str) -> ET.Element:
    q = ET.Element("question", type="category")
    cat = ET.SubElement(q, "category")
    text_el = ET.SubElement(cat, "text")
    text_el.text = f"$course$/top/{categoria}"
    return q


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", required=True, help="YAML de preguntas")
    ap.add_argument("--salida", required=True, help="XML de salida para importar en Moodle")
    args = ap.parse_args()

    with open(args.entrada, encoding="utf-8") as f:
        datos = yaml.safe_load(f)

    preguntas = datos.get("preguntas", [])
    if not preguntas:
        sys.exit("El YAML no tiene preguntas.")

    quiz = ET.Element("quiz")
    if datos.get("categoria"):
        quiz.append(construir_categoria(datos["categoria"]))
    for p in preguntas:
        quiz.append(construir_pregunta(p))

    xml_bytes = ET.tostring(quiz, encoding="utf-8")
    pretty = minidom.parseString(xml_bytes).toprettyxml(indent="  ", encoding="UTF-8")

    with open(args.salida, "wb") as f:
        f.write(pretty)

    print(f"{len(preguntas)} preguntas escritas en {args.salida}")


if __name__ == "__main__":
    main()
