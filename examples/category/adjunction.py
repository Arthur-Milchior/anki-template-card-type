
from .category import bareField
from ..util import addBoilerplate, bareFieldOrDefault, mathjax, mathjax_label, parenthese
from ...generators import *



c_in_C_name = "c in C (mathjax)"
c_in_LD_name = "c in LD (mathjax)"
c_in_LRC_name = "c in LRC (mathjax)"

d_in_D_mj_name = "d in D (mathjax)"

catC_mj = bareFieldOrDefault("Cat C (mathjax)", "\\mathcal C")
catD_mj = bareFieldOrDefault("Cat D (mathjax)", "\\mathcal D")
def C_mj(suffix=""):
    return bareFieldOrDefault(f"C{suffix} (mathjax)", f"C{suffix}")
def D_mj(suffix=""):
    return bareFieldOrDefault(f"D{suffix} (mathjax)", f"D{suffix}")
c_in_C_mj = bareFieldOrDefault(c_in_C_name, "c")
d_in_RC_mj = bareFieldOrDefault("d in RC (mathjax)", "d")
c_in_LRC_mj = bareFieldOrDefault(c_in_LRC_name, "c")
f_C_mj = bareFieldOrDefault("f_C (Cat C(C C')) (mathjax)", "f_c")
d_in_D_mj = bareFieldOrDefault(d_in_D_mj_name, "d")
c_in_LD_mj = bareFieldOrDefault(c_in_LD_name, "c")
f_D_mj = bareFieldOrDefault("f_D (Cat D(D D')) (mathjax)", "f_d")
def L_mj(base:bool):
    return  "L" if base else  bareFieldOrDefault("L (Cat D to Cat C) (mathjax)", "L")
def R_mj(base: bool):
    return "R" if base else bareFieldOrDefault("R (Cat C to Cat D) (mathjax)", "R")
fC_mj = bareFieldOrDefault("F_C (Cat C(LD C)) (mathjax)", "F(C)")
fD_mj = bareFieldOrDefault("F_D (Cat D(D RC)) (mathjax)", "F(D)")
def RC_formal_mj(base:bool, suffix=""):
    return [R_mj(base), parenthese(C_mj(suffix))]
def LD_formal_mj(base:bool, suffix=""):
    return [L_mj(base), parenthese(D_mj(suffix))]
LRC_formal_mj = [L_mj(base=False), parenthese(RC_formal_mj(base=False))]
RLD_formal_mj = [R_mj(base=False), parenthese(LD_formal_mj(base=False))]


hom_set_in_D_mj = [catD_mj, "(", D_mj(), ",", D_mj("'"), ")"]
hom_set_in_C_mj = [catC_mj, "(", C_mj(), ", ", C_mj("'"), ") "]

L_name = "L (Cat D to Cat C)"
R_name = "R (Cat C to Cat D)"
LD = "LD (C)"
RC = "RC (D)"
Lf_D = "Lf_D (Cat C(LD LD'))"
Rf_C = "Rf_C (Cat D(RC RC'))"
Lf_D_Ld = "(Lf_D)(c in LD) (LD')"
Rf_C_Rc = "(Rf_C)(d in RC) (RC')"
def LD_mj_name(suffix=""):
    return f"LD{suffix} (mathjax)"
def RC_mj_name(suffix=""):
    return f"RC{suffix} (mathjax)"
RLD_mj_name ="RLD (mathjax)"
LRC_mj_name ="LRC (mathjax)"

def LD_long_mj(base: bool, suffix=""):
    return [LD_formal_mj(base, suffix), Filled (LD_mj_name(suffix), ["=", bareField(LD_mj_name(suffix))])]
def RC_long_mj(base, suffix=""):
    return [RC_formal_mj(base, suffix), Filled (RC_mj_name(suffix), ["=", bareField(RC_mj_name(suffix))])]
RLD_long_mj = [RLD_formal_mj, Filled (RLD_mj_name, ["=", bareField(RLD_mj_name)])]
LRC_long_mj = [LRC_formal_mj, Filled (LRC_mj_name, ["=", bareField(LRC_mj_name)])]

def LD_short_mj(suffix=""):
    return (LD_mj_name(suffix), bareField(LD_mj_name(suffix)), LD_formal_mj(base=False, suffix=suffix))
def RC_short_mj(suffix=""):
    return (RC_mj_name(suffix), bareField(RC_mj_name(suffix)), RC_formal_mj(base=False, suffix=suffix))
RLD_short_mj = (RLD_mj_name, bareField(RLD_mj_name), RLD_formal_mj)
LRC_short_mj = (LRC_mj_name, bareField(LRC_mj_name), LRC_formal_mj)



def LD_mj(base:bool, suffix="'"):
    return LD_formal_mj(base, suffix) if base else LD_long_mj(base=base, suffix=suffix)

def RC_mj(base:bool, suffix=""):
    return RC_formal_mj(base, suffix) if base else RC_long_mj(suffix)

def lr(base:bool):
    return [
             {
                 "field": L_name,
                 "label": mathjax_label([L_mj(base=base), "\\in[", catD_mj, " , ", catC_mj, "]"]),
             },
             {
                 "field": LD,
                 "label": 
                      mathjax_label(L_mj(base=base),parenthese(D_mj() ), "\\in ",catC_mj, )
                 
             },
             {
                 "field": Lf_D,
                 "label": 
                      mathjax_label(L_mj(base=base),parenthese(f_D_mj ),"\\in ",catC_mj, "(", LD_mj(base), ", ", LD_mj(base, "'"),")")
                 
             },
             {
                 "field": Lf_D_Ld,
                 "label": 
                      mathjax_label("(",L_mj(base=base),parenthese(f_D_mj ),")",parenthese(c_in_LD_mj),"\\in", LD_mj(base, "'"),)
                 
             },
             {
                 "field": R_name,
                 "label": 
                      mathjax_label(R_mj(base=base), "\\in[", catC_mj, " , ", catD_mj, "]")
                 
             },
             {
                 "field": RC,
                 "label": 
                      mathjax_label(R_mj(base=base), parenthese(C_mj() ), "\\in ", catD_mj, )
                 
             },
             {
                 "field": Rf_C,
                 "label": 
                      mathjax_label(R_mj(base=base), parenthese(f_C_mj ), "\\in ", catD_mj, "(", RC_mj(base), ", ", RC_mj(base, "'"), ")")
                 
             },
             {
                 "field": Rf_C_Rc,
                 "label": 
                      mathjax_label("(", R_mj(base=base), parenthese(f_C_mj ), ")", parenthese(d_in_RC_mj), "\\in", RC_mj(base, "'"), )
             },
]

def _make_adjunction(ls, vars):
    return addBoilerplate([H5(["Adjunction"]), hr,
     [[TableFields(
         name="Adjunction",
         fields=l),hr] for l in ls]], 
         extra_variables = vars
)

var_cat = Filled("Cat C", [{"Cat C"}, {"Cat D"}])
var_object = [[ mathjax( C_mj(), "\\in ", catC_mj, )], ", ", [ mathjax( D_mj(), "\\in ", catD_mj, )],]
var_function = [
        [ mathjax( f_C_mj, "\\in ",  hom_set_in_C_mj, )], ",", [ mathjax( f_D_mj, "\\in ", hom_set_in_D_mj, )]]

def var_content_base(base: bool):
    return [
         Filled(
             c_in_LD_name, 
             [br, 
              [ mathjax( c_in_LD_mj, "\\in ", LD_mj(base), )], ",",
              [ mathjax( d_in_RC_mj, "\\in ", RC_mj(base), )],
            ]
          )
        ]

def var_base(base:bool):
    return [var_object, br, var_function, var_content_base(base)]

RLD = "RLD"
LRC = "LRC"
Lf_C_L_c = "(Lf_C)(Lc) (LC')"
Lf_D_L_d = "(Lf_D)(Ld) (LD')"
epsilon = "epsilon (LR to 1_Cat C)"
epsilon_C = "epsilon_C (LRC to C)"
epsilon_Cc = "epsilon_C(c in LRC) (C)"
eta = "eta (1_Cat D to RL)"
eta_D = "eta_D (D to RLD)"
eta_Dd = "eta_D(d in D) (RLD)"
Ld = "LD (C)"
Lf_d = "Lf_D (Cat C(L(D) L(D'))"
Rc = "RC (D)"
Rf_c = "Rf_C (Cat D(R(C) R(C')))"



adjunction_base = _make_adjunction([lr(base=True)], var_base(base=True))

_lr = lr(base=False)

_eta = [
            {
                "field": RLD,
                "label": 
                     mathjax_label( RLD_formal_mj, "\\in ", catD_mj, ),
                
                "hideInSomeQuestions": {LRC},
            },
            {
                "field": eta,
                "label": 
                     mathjax_label("\\eta\\in \mathrm{id}_{", catD_mj, "}\\to ", R_mj(base=False), "\\circ ", L_mj(base=False), ),
                
                "hideInSomeQuestions": {RLD, LRC},
            },
            {
                "field": eta_D,
                "label": 
                     mathjax_label("\\eta_{", D_mj(), "}\\in ", catD_mj, "(", D_mj(), ", ", RLD_long_mj, ")"),
                
                "hideInSomeQuestions": {RLD, LRC},
            },
            {
                "field": eta_Dd,
                "label": 
                     mathjax_label("\\eta_{", D_mj(), "}", parenthese(d_in_D_mj), "\\in ", RLD_long_mj, ),
                
                "hideInSomeQuestions": {RLD, LRC},
            },
] 
_epsilon = [
            {
                "field": LRC,
                "label":
                     mathjax_label( LRC_formal_mj, "\\in ", catC_mj,),
        
                "hideInSomeQuestions": {RLD},
            },
            {
                "field": epsilon,
                "label": 
                     mathjax_label("\\varepsilon\\in ", L_mj(base=False), " \\circ ", R_mj(base=False), "\\to \mathrm{id}_{", catC_mj, "}"),
                "hideInSomeQuestions": {LRC, RLD},
            },
            {
                "field": epsilon_C,
                "label": 
                     mathjax_label("\\varepsilon_{", C_mj(), "} \\in ", catC_mj,  "(", LRC_long_mj, ",", C_mj(), ")"),             
                "hideInSomeQuestions": {LRC, RLD},
            },
            {
                "field": epsilon_Cc,
                "label": 
                     mathjax_label("\\varepsilon_{", C_mj(), "}", parenthese(c_in_LRC_mj), "\\in ", C_mj(), )
                ,
                "hideInSomeQuestions": {LRC, RLD},
            },
        ]

def d_in_D_mj_var(suffix=emptyGen):
    return Filled(d_in_D_mj_name, mathjax(d_in_D_mj, "\\in ", D_mj(),) ,suffix)

var_eta=[
    d_in_D_mj_var(),
    Filled(c_in_LRC_name,    [", ", mathjax(c_in_LRC_mj, "\\in ", LRC_formal_mj, )])
]

adjunction_eta = _make_adjunction([_lr, _eta], [var_base(base=False), var_eta])
adjunction_epsilon = _make_adjunction([_lr, _epsilon], [var_base(base=False)])

overline_F_C = "overline F_C (Cat D(D RC))"
overline_F_Cd = "overline F_C(d) (RC)"
overline_F_D = "overline F_D (Cat C(LD C))"
overline_F_D_L_d = "overline F_D(Ld) (C)"


hom_set_equivalence_in_D_mj = [catD_mj, "(", D_mj(), ",", RC_short_mj(), ")"]
hom_set_equivalence_in_C_mj = [catC_mj, "(", LD_short_mj(), ", ", C_mj(), ") "]
_equivalence = [
             {
                 "field": overline_F_C,
                 "label": 
                      mathjax_label("\\overline{", fC_mj, "} \\in ", hom_set_equivalence_in_D_mj, ), 
                 
             },
             {
                 "field": overline_F_Cd,
                 "label": 
                      mathjax_label("\\overline{", fC_mj, "}", parenthese(d_in_D_mj), "\\in ", RC_short_mj(), ), 
                 
             },
             {
                 "field": overline_F_D,
                 "label": 
                      mathjax_label("\\overline{", fD_mj, "} \\in ", hom_set_equivalence_in_C_mj, ), 
                 
             },
             {
                 "field": overline_F_D_L_d,
                 "label": 
                      mathjax_label("\\overline{", fD_mj, "}", parenthese(c_in_LD_mj), "\\in ", C_mj(), ), 
                 
             },
]
var_content_bar = [br,
    d_in_D_mj_var(br),
    mathjax( fC_mj, "\\in", hom_set_equivalence_in_C_mj, ), ",",
    mathjax( fD_mj, "\\in", hom_set_equivalence_in_D_mj, ),
   ]
adjunction_equivalence = _make_adjunction([_lr , _equivalence], [var_base(base=False), var_content_bar])


all = [_lr, _eta+_epsilon, _equivalence
            #  {
            #      "field": "Isomorphism from hom_D(d,Rc) to hom_C(Ld,c)",
            #      "label": [
            #           mathjax("\\mathrm{Hom}_{", D, "}(", d2, ",", R, c1, ") \\to \\mathrm{Hom}_", C, "(", L, d2, ",", c1, ")")
            #      ],
            #  },
            #  {
            #      "field": "Isomorphism from hom_C(Ld,c) to hom_D(d,Rc)",
            #      "label": [
            #           mathjax("\\mathrm{Hom}_", C, "(", L, d2, ",", c1, ") \\to \\mathrm{Hom}_{", D, "}(", d2, ",", R, c1, ") ")
            #      ],
            #  },
         ]
adjunction = _make_adjunction(all,[var_base(base=False), var_eta, var_content_bar])