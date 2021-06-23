Each file correspond to one kind of tag.

Each file must:
* have a method compile_(tag, soup, **kwargs). It adds the content to the tag, and return the string of new contents. It may assume there is no content currently. kwargs may be arguments used for other modules.
* Have a method clean(tag), cleaning params potentially added by this module. The contents is cleaned by the caller.
* call templates.addKindOfTemplate(templateParameter, sys.modules[__name__]), stating that if «tempplate = templateParameter» occurs in a Span tag, the current module must be used on it.

The main template right now is "config". This allow to request a generator from the configuration file, and use to generate the content of this tag. It takes as paramater "name", for the name of the object in the configuration. "asked", for the comma-separated list of names asked. "hide" for the comma-separated list of names to hide.

Similar to "config", you have a template called "eval". Its attribute are the same than "config", but its name may be any python expression. (Note that your template must still be valid html. It means that if you have double quote «"» in your python expression, either those double quotes must be replaced by «&quot;», or the attribute must be surrounded by simple quotes «'».) The context in which this expression is evaluated contains every generators classes, and everything defined in the configuration. The effect depends on the type evaluated:
* if the result of the evaluation is a generator gen, then gen.template is called, with the current model, question side, and asked and hide, according to the attribute of this tag.
* if the result of a evaluation is a function, this function is called, the evaluation is then restarted according to the rules of eval. At most 10 such function called are done before the evaluation is aborted.
* if the result of the evaluation is a string, it is printed as-is in the html tag. HTML is escaped, thus <, > and & becomes &lt;, &gt; and &amp;.
* if the result of the evaluation is None, then nothing is done.
* if the result is of anothe type, it is evaluated according to the general rules of generators. (More precisely, according to generators.generators.ensureGen.

The other kind of template we currently consider are
* instruction: execute an arbitrary python expression. Context is the same as in eval. For example, you may use it to print, and thus debug things. Or to import a package. Note that this instruction is executed each time the template is compiled (and not executed during cleaning).
* fix: its content is not modified. Neither during compilation, nor during cleaning. (Note that if some descendants are also templates to edit, they will be edited. And if some ancestors are template to edit, this template may be deleted. So probably useless right now.)
* front side: the equivalent of {{FrontSide}}. But adapted to the fact that it is a question side.
* string: contains an arbitrary string in attribute string. Probably useless

Current keywords arguments passed are:
* isQuestion: whether the template appears on question side
* model: the model from which it is called
* objects: the list of objects defined in the config.
* FrontSide: the front side related to this backside