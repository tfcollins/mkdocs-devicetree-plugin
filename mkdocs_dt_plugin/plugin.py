import os
import sys

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

import yaml
from jinja2 import Environment, FileSystemLoader
import re


class DeviceTreePlugin(BasePlugin):

    config_scheme = (("param", config_options.Type(str, default="")),)

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_page_markdown(self, markdown, page, config, files):
        lines = markdown.split("\n")
        token = "::: linux"
        outs = []
        for line in lines:
            if token in line:
                out = line.split(token)[1]
                out = out.split(":")[1]
                _, props = self.process_yaml(out)

                # Add table marker for HTML insert pass
                outs.append(f"# {props['title']}\n")
                outs.append(f"{props['description']}\n")
                outs.append('\n=== "Properties"\n')
                line = f"    <!-- REPLACEME |{out}| -->\n"
                outs.append(line)
                outs.append('\n=== "Examples"\n')
                for ex in props["examples"]:
                    all = []
                    for e in ex.split("\n"):
                        all.append(f"    {e}")
                    ex = "\n".join(all)
                    outs.append(f"    ```yaml\n{ex}\n    ```")
            else:
                outs.append(line)
        markdown = "\n".join(outs)
        return markdown

    def process_yaml(self, filename):

        with open(filename, "r") as stream:
            data = yaml.safe_load(stream)

        if "description" in data:
            # replace link
            dec = data["description"]
            alls = []
            for s in dec.split(" "):
                if s.startswith("http"):
                    print(s)
                    v = s.split("/")[-1]
                    if "." in v:
                        v = v.split(".")[0]
                    s = s.replace(s, f"<a href='{s}'>{v}</a>")
                alls.append(s)

            dec = " ".join(alls)
            alls = []
            for s in dec.split("\n"):
                if s.startswith("http"):
                    print(s)
                    v = s.split("/")[-1]
                    if "." in v:
                        v = v.split(".")[0]
                    s = s.replace(s, f"<a href='{s}'>{v}</a>")
                alls.append(s)
            data["description"] = " ".join(alls)

        # Update required
        rq = data["required"]
        for prop in data["properties"]:
            if isinstance(data["properties"][prop], bool):
                v = data["properties"][prop]
                data["properties"][prop] = {
                    "required": "yes" if prop in rq else "",
                    "description": "",
                    "type": "bool",
                }
            elif isinstance(data["properties"][prop], dict):
                if rq:
                    data["properties"][prop]["required"] = "yes" if prop in rq else ""
                else:
                    data["properties"][prop]["required"] = ""

                if "enum" in data["properties"][prop]:
                    data["properties"][prop]["type"] = "enum"
                    if "description" in data["properties"][prop]:
                        dec = data["properties"][prop]["description"]
                    else:
                        dec = ""
                    if len(dec) > 0:
                        en = "<br>Options: "
                    else:
                        en = "Options: "

                    for e in data["properties"][prop]["enum"]:
                        en += f"<span class='enum-dt'>&nbsp{e}&nbsp</span> "
                    data["properties"][prop]["description"] = dec + en
            else:
                t = str(type(data["properties"][prop]))
                raise Exception(f"Unknown prop type: {prop} {t}")

        loc = os.path.dirname(__file__)
        loc = os.path.join(loc, "templates")
        file_loader = FileSystemLoader(loc)
        env = Environment(loader=file_loader)

        loc = os.path.join("prop_table.html")
        template = env.get_template(loc)

        output = template.render(data=data)
        return output, data

    def on_page_content(self, html, page, config, files):

        outs = []
        token = "<!-- REPLACEME"
        for line in html.split("\n"):
            if token in line:
                v = line.split("|")[1]
                line, _ = self.process_yaml(v)
            outs.append(line)
        html = "\n".join(outs)

        return html
