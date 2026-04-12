from pathlib import Path
import json
import re

current = Path(__file__).resolve()

for parent in current.parents:
    if (parent / "questions.json").exists():
        base_dir = parent
        break
else:
    raise FileNotFoundError("questions.json não encontrado em diretórios pais")

json_path = base_dir / "questions.json"
output_dir = base_dir / "../../questions"

print("BASE DIR:", base_dir)
print("JSON PATH:", json_path)

output_dir.mkdir(exist_ok=True)

def format_latex(text: str) -> str:
    text = text.strip()

    text = re.sub(
        r"(?<!\n)(\\begin\{[^}]+\}|\\end\{[^}]+\}|\\[a-zA-Z@]+[*]?)",
        r"\n\1",
        text
    )

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    formatted = []
    indent = 0

    for line in lines:

        if re.match(r"\\end\{", line):
            indent -= 1

        formatted.append("    " * max(indent, 0) + line)

        if re.match(r"\\begin\{", line):
            indent += 1

    return "\n".join(formatted)


with json_path.open("r", encoding="utf-8") as f:
    questions = json.load(f)

for i, item in enumerate(questions, start=1):
    q = str(item.get("question", "")).strip()
    a = str(item.get("answer", "")).strip()

    a = format_latex(a)

    file_path = output_dir / f"{i}_question.tex"

    file_path.write_text(
        f"\\displayQuestionOnScreen{{{q}}}{{{a}}}\n",
        encoding="utf-8"
    )

print(f"✅ Sucesso! {len(questions)} arquivos gerados em: {output_dir}")