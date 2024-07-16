#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Annotated, Union

import typer
import json
from peft import AutoPeftModelForCausalLM, PeftModelForCausalLM
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

ModelType = Union[PreTrainedModel, PeftModelForCausalLM]
TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]

app = typer.Typer(pretty_exceptions_show_locals=False)


def _resolve_path(path: Union[str, Path]) -> Path:
    return Path(path).expanduser().resolve()


def load_model_and_tokenizer(model_dir: Union[str, Path]) -> tuple[ModelType, TokenizerType]:
    model_dir = _resolve_path(model_dir)
    if (model_dir / 'adapter_config.json').exists():
        model = AutoPeftModelForCausalLM.from_pretrained(
            model_dir, trust_remote_code=True, device_map='auto'
        )
        tokenizer_dir = model.peft_config['default'].base_model_name_or_path
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_dir, trust_remote_code=True, device_map='auto'
        )
        tokenizer_dir = model_dir
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_dir, trust_remote_code=True
    )
    return model, tokenizer


@app.command()
def main(
        model_dir: Annotated[str, typer.Argument(help='')],
        test_file: Annotated[str, typer.Option(help='')],
        output_file: Annotated[str, typer.Option(help='')],
):
    model, tokenizer = load_model_and_tokenizer(model_dir)
    f = open(test_file, 'r', encoding = 'utf_8')
    f_out = open(output_file, 'w', encoding = 'utf_8')
    line = 0
    for each in f:
        line += 1
        jdata = json.loads(each)
        prompt = jdata['conversations'][0]['content']
        response, _ = model.chat(tokenizer, prompt)
        print(line, response)
        data ={
		    "conversations": [
                {"role": "user",
                "content": "{}{}".format("请将下文解析成CQL语句：\n", prompt)
                    }, 
                {"role": "assistant", 
                    "content": "{}".format(response)
                    }
				]
			}
        item = json.dumps(data, ensure_ascii=False)
        f_out.write("{}\n".format(item))
    f.close()
    f_out.close()

    f = open(test_file, 'r', encoding = 'utf_8')
    map_input = {}
    for each in f:
        jdata = json.loads(each)
        prompt = jdata['conversations'][0]['content']
        prompt = prompt.split('\n')[-1]
        sql =  jdata['conversations'][1]['content']
        map_input[prompt] = sql
    map_out = {}
    f_out = open(output_file, 'r', encoding = 'utf_8')
    r = 0
    for each in f_out:
        jdata = json.loads(each)
        prompt = jdata['conversations'][0]['content']
        prompt = prompt.split('\n')[-1]
        sql =  jdata['conversations'][1]['content']
        if map_input[prompt] == sql:
            r += 1
        map_out[prompt] = sql

    print(r/len(map_input), r, len(map_input))
    

if __name__ == '__main__':
    app()
