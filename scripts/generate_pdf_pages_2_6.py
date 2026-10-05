from pathlib import Path
import fitz

src = Path(r"C:\Users\aledi\OneDrive\Documentos\Alejandra\Trabajo\COLFLUX\Repositorio\context\files\objetivo3\Qué es COLFLUX.pdf")
dst = Path(r"C:\Users\aledi\OneDrive\Documentos\Alejandra\Trabajo\COLFLUX\Repositorio\context\docs\assets\pdf\que-es-colflux-pag2-6.pdf")

if not src.exists():
    raise FileNotFoundError(f"No se encontró el PDF original: {src}")

doc = fitz.open(str(src))
if doc.page_count < 6:
    raise ValueError(f"El PDF original tiene solo {doc.page_count} páginas y no alcanza 2 a 6.")

out = fitz.open()
for page_index in range(1, 6):
    out.insert_pdf(doc, from_page=page_index, to_page=page_index)

out.save(str(dst))
print(f"PDF generado: {dst}")
print(f"Páginas creadas: {out.page_count}")
