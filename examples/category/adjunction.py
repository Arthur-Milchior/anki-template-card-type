
from .category import bareField
from ..util import addBoilerplate, bareFieldOrDefault
from ...generators import *

c_in_C_name = "c in C (mathjax)"
c_in_LD_name = "c in LD (mathjax)"
c_in_LRC_name = "c in LRC (mathjax)"

catC_mj = bareFieldOrDefault("Cat C (mathjax)", "\\mathcal C")
catD_mj = bareFieldOrDefault("Cat D (mathjax)", "\\mathcal D")
C_mj = bareFieldOrDefault("C (mathjax)", "C")
D_mj = bareFieldOrDefault("D (mathjax)", "D")
C2_mj = bareFieldOrDefault("C' (mathjax)", "C'")
D2_mj = bareFieldOrDefault("D' (mathjax)", "D'")
c_in_C_mj = bareFieldOrDefault(c_in_C_name, "c")
d_in_RC_mj = bareFieldOrDefault("d in RC (mathjax)", "d")
c_in_LRC_mj = bareFieldOrDefault(c_in_LRC_name, "c")
f_C_mj = bareFieldOrDefault("f_C (Cat C(C C')) (mathjax)", "f_c")
d_in_D_mj = bareFieldOrDefault("d in D (mathjax)", "d")
c_in_LD_mj = bareFieldOrDefault(c_in_LD_name, "c")
f_D_mj = bareFieldOrDefault("f_D (Cat D(D D')) (mathjax)", "f_d")
L_mj = bareFieldOrDefault("L (Cat D to Cat C) (mathjax)", "L")
R_mj = bareFieldOrDefault("R (Cat C to Cat D) (mathjax)", "R")
fC_mj = bareFieldOrDefault("F_C (Cat C(LD C)) (mathjax)", "F(C)")
fD_mj = bareFieldOrDefault("F_D (Cat D(D RC)) (mathjax)", "F(D)")
RC_mj = [R_mj, "(", C_mj, ")"]
LD_mj = [L_mj, "(", D_mj, ")"]
LRC_mj = [L_mj, "(", RC_mj, ")"]
RLD_mj = [R_mj, "(", LD_mj, ")"]


hom_set_in_D_mj = [catD_mj, "(", D_mj, ",", RC_mj, ")"]
hom_set_in_C_mj = [catC_mj, "(", LD_mj, ", ", C_mj, ") "]

L_name = "L (Cat D to Cat C)"
R_name = "R (Cat C to Cat D)"
LD = "LD (C)"
RC = "RC (D)"
Lf_D = "Lf_D (Cat C(LD LD'))"
Rf_C = "Rf_C (Cat D(RC RC'))"
Lf_D_Ld = "(Lf_D)(Ld) (LD')"
Rf_C_Rc = "(Rf_C)(Rc) (RC')"

def lr(left, right):
    LD_mj = [left, "(", D_mj, ")"]
    RC_mj = [right, "(", C_mj, ")"]
    LD2_mj = [left, "(", D2_mj, ")"]
    RC2_mj = [right, "(", C2_mj, ")"]
    return [
             {
                 "field": L_name,
                 "label": [
                     "\\(",left, "\\in[", catD_mj, " , ", catC_mj, "]\\): "
                 ],
             },
             {
                 "field": LD,
                 "label": [
                     "\\(",left,"(", D_mj ,")", "\\in ",catC_mj, "\\): "
                 ],
             },
             {
                 "field": Lf_D,
                 "label": [
                     "\\(",left,"(", f_D_mj ,")\\in ",catC_mj, "(", LD_mj, ", ", LD2_mj,")\\): "
                 ],
             },
             {
                 "field": Lf_D_Ld,
                 "label": [
                     "\\((",left,"(", f_D_mj ,"))(",  c_in_LD_mj, ")\\in", LD2_mj,"\\):"
                 ],
             },
             {
                 "field": R_name,
                 "label": [
                     "\\(",right, "\\in[", catC_mj, " , ", catD_mj, "]\\): "
                 ],
             },
             {
                 "field": RC,
                 "label": [
                     "\\(",right,"(", C_mj ,")", "\\in ",catD_mj, "\\): "
                 ],
             },
             {
                 "field": Rf_C,
                 "label": [
                     "\\(",right,"(", f_C_mj ,")\\in ",catD_mj, "(", RC_mj, ", ", RC2_mj, ")\\): "
                 ],
             },
             {
                 "field": Rf_C_Rc,
                 "label": [
                     "\\((",right,"(", f_C_mj ,"))(", right, d_in_RC_mj, ")\\in", RC2_mj, "\\):"
                 ],
             },
]

def _make_adjunction(ls, vars):
    return addBoilerplate([H5(["Adjunction"]), hr,
     [[TableFields(
         name="Adjunction",
         fields=l),hr] for l in ls]], 
         extra_variables = vars
)

var_object = [["\\(", C_mj, "\\in ", catC_mj, "\\)"], ", ", ["\\(", D_mj, "\\in ", catD_mj, "\\)"],]
var_function = [
        ["\\(", fD_mj, "\\in ", hom_set_in_D_mj, "\\)"], ", " , ["\\(", fC_mj, "\\in ",  hom_set_in_C_mj, "\\)"]]
var_content_base = [
        #["\\(", c_in_C, "\\in ", C, "\\)"], ",", ["\\(", d_in_D, "\\in ", D, "\\)"],
         Filled(c_in_LD_name, [br, 
        ["\\(", c_in_LD_mj, "\\in ", L_mj,D_mj, "\\)"], ",", ["\\(", d_in_RC_mj, "\\in ", R_mj,C_mj, "\\)"],])
        ]

var_base = [var_object, br, var_function, Filled(c_in_C_name, [br, var_content_base])]

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

adjunction_base = _make_adjunction([lr("L", "R")], var_base)

_lr = lr(L_mj, R_mj)

_eta = [
            {
                "field": RLD,
                "label": [
                    "\\(", RLD_mj, "\\in ", catD_mj, "\\): "
                ],
                "hideInSomeQuestion": {LRC, epsilon},
            },
            {
                "field": eta,
                "label": [
                    "\\(\\eta\\in 1_{", catD_mj, "}\\to ", R_mj, "\\circ ", L_mj, "\\): "
                ],
                "hideInSomeQuestion": {RLD, LRC, epsilon},
            },
            {
                "field": eta_D,
                "label": [
                    "\\(\\eta_{", D_mj, "}\\in ", catD_mj, "(", D_mj, ", ", RLD_mj, ")\\): "
                ],
                "hideInSomeQuestion": {RLD, LRC, epsilon},
            },
            {
                "field": eta_Dd,
                "label": [
                    "\\(\\eta_{", D_mj, "}(", d_in_D_mj, ")\\in ", RLD_mj, "\\): "
                ],
                "hideInSomeQuestion": {RLD, LRC, epsilon},
            },
] 
_epsilon = [
            {
                "field": LRC,
                "label": [
                    "\\(", LRC_mj, "\\in ", catC_mj,"\\): "
                ],
                "hideInSomeQuestion": {RLD, eta},
            },
            {
                "field": epsilon,
                "label": [
                    "\\(\\varepsilon\\in ", L_mj, " \\circ ", R_mj, "\\to 1_{", catC_mj, "}\\): "
                ],
                "hideInSomeQuestion": {LRC, RLD, eta},
            },
            {
                "field": epsilon_C,
                "label": [
                    "\\(\\varepsilon_{", C_mj, "} \\in ", catC_mj,  "(", LRC_mj, ",", C_mj, ")\\): "
                ],
                "hideInSomeQuestion": {LRC, RLD, eta},
            },
            {
                "field": epsilon_Cc,
                "label": [
                    "\\(\\varepsilon_{", C_mj, "}(", c_in_LRC_mj, ")\\in ", C_mj, "\\): "
                ],
                "hideInSomeQuestion": {LRC, RLD, eta},
            },
        ]

var_epsilon=[
Filled(c_in_LRC_name,    [", \\(", c_in_LRC_mj, "\\in ", LRC_mj, "\\)"])
]

adjunction_eta = _make_adjunction([_lr, _eta], [var_base])
adjunction_epsilon = _make_adjunction([_lr, _epsilon], [var_base, var_epsilon])

overline_F_C = "overline F_C (Cat D(D RC))"
overline_F_Cd = "overline F_C(d) (RC)"
overline_F_D = "overline F_D (Cat C(LD C))"
overline_F_D_L_d = "overline F_D(Ld) (C)"

_equivalence = [
             {
                 "field": overline_F_C,
                 "label": [
                     "\\(\\overline{", fC_mj, "}\\in ", hom_set_in_D_mj, "\\):",
                 ],
             },
             {
                 "field": overline_F_Cd,
                 "label": [
                     "\\(\\overline{", fC_mj, "}(", d_in_D_mj,")\\in ", R_mj, "(", C_mj, ")" , "\\):",
                 ],
             },
             {
                 "field": overline_F_D,
                 "label": [
                     "\\(\\overline{", fD_mj, "}\\in ", hom_set_in_C_mj, "\\)",
                 ],
             },
             {
                 "field": overline_F_D_L_d,
                 "label": [
                     "\\(\\overline{", fD_mj, "}(", c_in_LD_mj,")\\in ", C_mj, "\\):",
                 ],
             },
]
var_content_bar = [br,
    ["\\(", fC_mj, "\\in", hom_set_in_C_mj, "\\)"], ",", ["\\(", fD_mj, "\\in", hom_set_in_D_mj, "\\)"],
   ]
adjunction_equivalence = _make_adjunction([_lr , _equivalence], [var_base,var_content_bar])


all = [_lr, _eta+_epsilon, _equivalence
            #  {
            #      "field": "Isomorphism from hom_D(d,Rc) to hom_C(Ld,c)",
            #      "label": [
            #          "\\(\\mathrm{Hom}_{", D, "}(", d2, ",", R, c1, ") \\to \\mathrm{Hom}_", C, "(", L, d2, ",", c1, ")\\)"
            #      ],
            #  },
            #  {
            #      "field": "Isomorphism from hom_C(Ld,c) to hom_D(d,Rc)",
            #      "label": [
            #          "\\(\\mathrm{Hom}_", C, "(", L, d2, ",", c1, ") \\to \\mathrm{Hom}_{", D, "}(", d2, ",", R, c1, ") \\)"
            #      ],
            #  },
         ]
adjunction = _make_adjunction(all,[var_base, var_epsilon, var_content_bar])