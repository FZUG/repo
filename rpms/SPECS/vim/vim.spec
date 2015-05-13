%define patchlevel 728
%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 1
%endif
%define desktop_file 1
%if %{desktop_file}
%define desktop_file_utils_version 0.2.93
%endif

%define withnetbeans 1

%define withvimspell 0
%define withhunspell 0
%define withruby 1
%define withlua 1

%define baseversion 7.4
%define vimdir vim74

Summary: The VIM editor
URL:     http://www.vim.org/
Name: vim
Version: %{baseversion}.%{patchlevel}
Release: 2%{?dist}
License: Vim
Group: Applications/Editors
Source0: ftp://ftp.vim.org/pub/vim/unix/vim-%{baseversion}.tar.bz2
Source3: gvim.desktop
Source4: vimrc
Source5: ftp://ftp.vim.org/pub/vim/patches/README.patches
Source7: gvim16.png
Source8: gvim32.png
Source9: gvim48.png
Source10: gvim64.png
Source11: Changelog.rpm
Source12: vi_help.txt
%if %{withvimspell}
Source13: vim-spell-files.tar.bz2
%endif
Source14: spec-template
Source15: spec-template.new

Patch2002: vim-7.0-fixkeys.patch
Patch2003: vim-6.2-specsyntax.patch
%if %{withhunspell}
Patch2011: vim-7.0-hunspell.patch
BuildRequires: hunspell-devel
%endif

Patch001: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.001
Patch002: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.002
Patch003: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.003
Patch004: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.004
Patch005: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.005
Patch006: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.006
Patch007: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.007
Patch008: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.008
Patch009: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.009
Patch010: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.010
Patch011: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.011
Patch012: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.012
Patch013: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.013
Patch014: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.014
Patch015: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.015
Patch016: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.016
Patch017: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.017
Patch018: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.018
Patch019: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.019
Patch020: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.020
Patch021: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.021
Patch022: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.022
Patch023: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.023
Patch024: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.024
Patch025: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.025
Patch026: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.026
Patch027: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.027
Patch028: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.028
Patch029: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.029
Patch030: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.030
Patch031: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.031
Patch032: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.032
Patch033: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.033
Patch034: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.034
Patch035: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.035
Patch036: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.036
Patch037: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.037
Patch038: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.038
Patch039: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.039
Patch040: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.040
Patch041: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.041
Patch042: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.042
Patch043: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.043
Patch044: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.044
Patch045: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.045
Patch046: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.046
Patch047: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.047
Patch048: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.048
Patch049: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.049
Patch050: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.050
Patch051: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.051
Patch052: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.052
Patch053: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.053
Patch054: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.054
Patch055: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.055
Patch056: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.056
Patch057: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.057
Patch058: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.058
Patch059: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.059
Patch060: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.060
Patch061: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.061
Patch062: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.062
Patch063: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.063
Patch064: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.064
Patch065: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.065
Patch066: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.066
Patch067: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.067
Patch068: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.068
Patch069: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.069
Patch070: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.070
Patch071: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.071
Patch072: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.072
Patch073: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.073
Patch074: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.074
Patch075: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.075
Patch076: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.076
Patch077: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.077
Patch078: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.078
Patch079: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.079
Patch080: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.080
Patch081: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.081
Patch082: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.082
Patch083: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.083
Patch084: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.084
Patch085: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.085
Patch086: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.086
Patch087: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.087
Patch088: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.088
Patch089: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.089
Patch090: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.090
Patch091: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.091
Patch092: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.092
Patch093: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.093
Patch094: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.094
Patch095: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.095
Patch096: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.096
Patch097: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.097
Patch098: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.098
Patch099: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.099
Patch100: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.100
Patch101: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.101
Patch102: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.102
Patch103: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.103
Patch104: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.104
Patch105: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.105
Patch106: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.106
Patch107: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.107
Patch108: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.108
Patch109: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.109
Patch110: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.110
Patch111: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.111
Patch112: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.112
Patch113: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.113
Patch114: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.114
Patch115: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.115
Patch116: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.116
Patch117: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.117
Patch118: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.118
Patch119: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.119
Patch120: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.120
Patch121: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.121
Patch122: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.122
Patch123: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.123
Patch124: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.124
Patch125: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.125
Patch126: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.126
Patch127: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.127
Patch128: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.128
Patch129: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.129
Patch130: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.130
Patch131: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.131
Patch132: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.132
Patch133: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.133
Patch134: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.134
Patch135: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.135
Patch136: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.136
Patch137: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.137
Patch138: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.138
Patch139: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.139
Patch140: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.140
Patch141: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.141
Patch142: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.142
Patch143: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.143
Patch144: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.144
Patch145: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.145
Patch146: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.146
Patch147: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.147
Patch148: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.148
Patch149: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.149
Patch150: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.150
Patch151: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.151
Patch152: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.152
Patch153: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.153
Patch154: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.154
Patch155: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.155
Patch156: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.156
Patch157: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.157
Patch158: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.158
Patch159: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.159
Patch160: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.160
Patch161: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.161
Patch162: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.162
Patch163: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.163
Patch164: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.164
Patch165: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.165
Patch166: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.166
Patch167: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.167
Patch168: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.168
Patch169: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.169
Patch170: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.170
Patch171: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.171
Patch172: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.172
Patch173: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.173
Patch174: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.174
Patch175: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.175
Patch176: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.176
Patch177: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.177
Patch178: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.178
Patch179: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.179
Patch180: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.180
Patch181: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.181
Patch182: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.182
Patch183: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.183
Patch184: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.184
Patch185: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.185
Patch186: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.186
Patch187: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.187
Patch188: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.188
Patch189: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.189
Patch190: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.190
Patch191: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.191
Patch192: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.192
Patch193: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.193
Patch194: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.194
Patch195: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.195
Patch196: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.196
Patch197: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.197
Patch198: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.198
Patch199: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.199
Patch200: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.200
Patch201: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.201
Patch202: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.202
Patch203: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.203
Patch204: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.204
Patch205: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.205
Patch206: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.206
Patch207: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.207
Patch208: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.208
Patch209: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.209
Patch210: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.210
Patch211: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.211
Patch212: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.212
Patch213: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.213
Patch214: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.214
Patch215: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.215
Patch216: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.216
Patch217: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.217
Patch218: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.218
Patch219: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.219
Patch220: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.220
Patch221: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.221
Patch222: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.222
Patch223: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.223
Patch224: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.224
Patch225: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.225
Patch226: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.226
Patch227: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.227
Patch228: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.228
Patch229: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.229
Patch230: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.230
Patch231: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.231
Patch232: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.232
Patch233: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.233
Patch234: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.234
Patch235: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.235
Patch236: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.236
Patch237: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.237
Patch238: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.238
Patch239: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.239
Patch240: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.240
Patch241: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.241
Patch242: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.242
Patch243: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.243
Patch244: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.244
Patch245: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.245
Patch246: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.246
Patch247: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.247
Patch248: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.248
Patch249: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.249
Patch250: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.250
Patch251: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.251
Patch252: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.252
Patch253: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.253
Patch254: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.254
Patch255: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.255
Patch256: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.256
Patch257: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.257
Patch258: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.258
Patch259: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.259
Patch260: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.260
Patch261: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.261
Patch262: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.262
Patch263: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.263
Patch264: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.264
Patch265: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.265
Patch266: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.266
Patch267: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.267
Patch268: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.268
Patch269: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.269
Patch270: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.270
Patch271: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.271
Patch272: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.272
Patch273: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.273
Patch274: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.274
Patch275: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.275
Patch276: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.276
Patch277: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.277
Patch278: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.278
Patch279: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.279
Patch280: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.280
Patch281: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.281
Patch282: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.282
Patch283: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.283
Patch284: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.284
Patch285: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.285
Patch286: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.286
Patch287: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.287
Patch288: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.288
Patch289: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.289
Patch290: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.290
Patch291: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.291
Patch292: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.292
Patch293: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.293
Patch294: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.294
Patch295: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.295
Patch296: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.296
Patch297: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.297
Patch298: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.298
Patch299: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.299
Patch300: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.300
Patch301: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.301
Patch302: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.302
Patch303: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.303
Patch304: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.304
Patch305: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.305
Patch306: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.306
Patch307: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.307
Patch308: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.308
Patch309: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.309
Patch310: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.310
Patch311: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.311
Patch312: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.312
Patch313: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.313
Patch314: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.314
Patch315: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.315
Patch316: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.316
Patch317: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.317
Patch318: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.318
Patch319: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.319
Patch320: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.320
Patch321: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.321
Patch322: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.322
Patch323: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.323
Patch324: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.324
Patch325: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.325
Patch326: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.326
Patch327: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.327
Patch328: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.328
Patch329: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.329
Patch330: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.330
Patch331: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.331
Patch332: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.332
Patch333: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.333
Patch334: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.334
Patch335: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.335
Patch336: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.336
Patch337: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.337
Patch338: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.338
Patch339: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.339
Patch340: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.340
Patch341: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.341
Patch342: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.342
Patch343: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.343
Patch344: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.344
Patch345: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.345
Patch346: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.346
Patch347: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.347
Patch348: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.348
Patch349: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.349
Patch350: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.350
Patch351: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.351
Patch352: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.352
Patch353: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.353
Patch354: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.354
Patch355: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.355
Patch356: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.356
Patch357: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.357
Patch358: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.358
Patch359: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.359
Patch360: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.360
Patch361: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.361
Patch362: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.362
Patch363: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.363
Patch364: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.364
Patch365: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.365
Patch366: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.366
Patch367: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.367
Patch368: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.368
Patch369: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.369
Patch370: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.370
Patch371: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.371
Patch372: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.372
Patch373: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.373
Patch374: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.374
Patch375: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.375
Patch376: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.376
Patch377: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.377
Patch378: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.378
Patch379: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.379
Patch380: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.380
Patch381: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.381
Patch382: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.382
Patch383: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.383
Patch384: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.384
Patch385: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.385
Patch386: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.386
Patch387: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.387
Patch388: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.388
Patch389: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.389
Patch390: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.390
Patch391: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.391
Patch392: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.392
Patch393: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.393
Patch394: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.394
Patch395: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.395
Patch396: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.396
Patch397: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.397
Patch398: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.398
Patch399: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.399
Patch400: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.400
Patch401: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.401
Patch402: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.402
Patch403: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.403
Patch404: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.404
Patch405: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.405
Patch406: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.406
Patch407: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.407
Patch408: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.408
Patch409: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.409
Patch410: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.410
Patch411: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.411
Patch412: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.412
Patch413: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.413
Patch414: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.414
Patch415: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.415
Patch416: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.416
Patch417: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.417
Patch418: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.418
Patch419: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.419
Patch420: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.420
Patch421: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.421
Patch422: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.422
Patch423: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.423
Patch424: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.424
Patch425: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.425
Patch426: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.426
Patch427: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.427
Patch428: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.428
Patch429: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.429
Patch430: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.430
Patch431: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.431
Patch432: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.432
Patch433: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.433
Patch434: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.434
Patch435: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.435
Patch436: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.436
Patch437: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.437
Patch438: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.438
Patch439: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.439
Patch440: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.440
Patch441: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.441
Patch442: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.442
Patch443: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.443
Patch444: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.444
Patch445: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.445
Patch446: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.446
Patch447: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.447
Patch448: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.448
Patch449: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.449
Patch450: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.450
Patch451: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.451
Patch452: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.452
Patch453: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.453
Patch454: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.454
Patch455: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.455
Patch456: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.456
Patch457: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.457
Patch458: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.458
Patch459: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.459
Patch460: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.460
Patch461: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.461
Patch462: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.462
Patch463: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.463
Patch464: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.464
Patch465: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.465
Patch466: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.466
Patch467: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.467
Patch468: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.468
Patch469: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.469
Patch470: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.470
Patch471: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.471
Patch472: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.472
Patch473: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.473
Patch474: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.474
Patch475: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.475
Patch476: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.476
Patch477: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.477
Patch478: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.478
Patch479: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.479
Patch480: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.480
Patch481: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.481
Patch482: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.482
Patch483: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.483
Patch484: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.484
Patch485: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.485
Patch486: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.486
Patch487: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.487
Patch488: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.488
Patch489: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.489
Patch490: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.490
Patch491: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.491
Patch492: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.492
Patch493: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.493
Patch494: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.494
Patch495: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.495
Patch496: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.496
Patch497: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.497
Patch498: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.498
Patch499: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.499
Patch500: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.500
Patch501: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.501
Patch502: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.502
Patch503: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.503
Patch504: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.504
Patch505: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.505
Patch506: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.506
Patch507: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.507
Patch508: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.508
Patch509: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.509
Patch510: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.510
Patch511: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.511
Patch512: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.512
Patch513: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.513
Patch514: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.514
Patch515: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.515
Patch516: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.516
Patch517: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.517
Patch518: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.518
Patch519: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.519
Patch520: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.520
Patch521: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.521
Patch522: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.522
Patch523: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.523
Patch524: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.524
Patch525: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.525
Patch526: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.526
Patch527: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.527
Patch528: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.528
Patch529: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.529
Patch530: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.530
Patch531: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.531
Patch532: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.532
Patch533: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.533
Patch534: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.534
Patch535: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.535
Patch536: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.536
Patch537: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.537
Patch538: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.538
Patch539: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.539
Patch540: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.540
Patch541: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.541
Patch542: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.542
Patch543: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.543
Patch544: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.544
Patch545: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.545
Patch546: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.546
Patch547: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.547
Patch548: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.548
Patch549: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.549
Patch550: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.550
Patch551: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.551
Patch552: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.552
Patch553: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.553
Patch554: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.554
Patch555: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.555
Patch556: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.556
Patch557: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.557
Patch558: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.558
Patch559: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.559
Patch560: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.560
Patch561: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.561
Patch562: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.562
Patch563: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.563
Patch564: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.564
Patch565: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.565
Patch566: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.566
Patch567: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.567
Patch568: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.568
Patch569: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.569
Patch570: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.570
Patch571: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.571
Patch572: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.572
Patch573: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.573
Patch574: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.574
Patch575: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.575
Patch576: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.576
Patch577: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.577
Patch578: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.578
Patch579: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.579
Patch580: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.580
Patch581: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.581
Patch582: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.582
Patch583: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.583
Patch584: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.584
Patch585: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.585
Patch586: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.586
Patch587: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.587
Patch588: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.588
Patch589: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.589
Patch590: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.590
Patch591: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.591
Patch592: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.592
Patch593: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.593
Patch594: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.594
Patch595: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.595
Patch596: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.596
Patch597: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.597
Patch598: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.598
Patch599: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.599
Patch600: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.600
Patch601: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.601
Patch602: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.602
Patch603: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.603
Patch604: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.604
Patch605: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.605
Patch606: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.606
Patch607: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.607
Patch608: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.608
Patch609: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.609
Patch610: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.610
Patch611: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.611
Patch612: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.612
Patch613: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.613
Patch614: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.614
Patch615: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.615
Patch616: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.616
Patch617: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.617
Patch618: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.618
Patch619: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.619
Patch620: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.620
Patch621: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.621
Patch622: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.622
Patch623: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.623
Patch624: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.624
Patch625: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.625
Patch626: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.626
Patch627: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.627
Patch628: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.628
Patch629: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.629
Patch630: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.630
Patch631: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.631
Patch632: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.632
Patch633: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.633
Patch634: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.634
Patch635: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.635
Patch636: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.636
Patch637: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.637
Patch638: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.638
Patch639: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.639
Patch640: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.640
Patch641: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.641
Patch642: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.642
Patch643: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.643
Patch644: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.644
Patch645: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.645
Patch646: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.646
Patch647: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.647
Patch648: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.648
Patch649: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.649
Patch650: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.650
Patch651: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.651
Patch652: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.652
Patch653: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.653
Patch654: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.654
Patch655: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.655
Patch656: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.656
Patch657: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.657
Patch658: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.658
Patch659: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.659
Patch660: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.660
Patch661: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.661
Patch662: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.662
Patch663: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.663
Patch664: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.664
Patch665: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.665
Patch666: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.666
Patch667: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.667
Patch668: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.668
Patch669: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.669
Patch670: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.670
Patch671: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.671
Patch672: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.672
Patch673: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.673
Patch674: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.674
Patch675: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.675
Patch676: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.676
Patch677: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.677
Patch678: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.678
Patch679: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.679
Patch680: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.680
Patch681: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.681
Patch682: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.682
Patch683: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.683
Patch684: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.684
Patch685: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.685
Patch686: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.686
Patch687: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.687
Patch688: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.688
Patch689: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.689
Patch690: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.690
Patch691: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.691
Patch692: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.692
Patch693: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.693
Patch694: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.694
Patch695: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.695
Patch696: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.696
Patch697: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.697
Patch698: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.698
Patch699: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.699
Patch700: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.700
Patch701: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.701
Patch702: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.702
Patch703: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.703
Patch704: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.704
Patch705: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.705
Patch706: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.706
Patch707: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.707
Patch708: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.708
Patch709: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.709
Patch710: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.710
Patch711: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.711
Patch712: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.712
Patch713: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.713
Patch714: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.714
Patch715: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.715
Patch716: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.716
Patch717: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.717
Patch718: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.718
Patch719: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.719
Patch720: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.720
Patch721: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.721
Patch722: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.722
Patch723: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.723
Patch724: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.724
Patch725: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.725
Patch726: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.726
Patch727: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.727
Patch728: ftp://ftp.vim.org/pub/vim/patches/7.4/7.4.728

Patch1559: 7.4.559.rhpatched
Patch3000: vim-7.4-syntax.patch
Patch3002: vim-7.1-nowarnings.patch
Patch3004: vim-7.0-rclocation.patch
Patch3006: vim-6.4-checkhl.patch
Patch3007: vim-7.4-fstabsyntax.patch
Patch3008: vim-7.0-warning.patch
Patch3009: vim-7.4-syncolor.patch
Patch3010: vim-7.0-specedit.patch
Patch3011: vim72-rh514717.patch
Patch3012: vim-7.3-manpage-typo-668894-675480.patch
Patch3013: vim-manpagefixes-948566.patch
Patch3014: vim-7.4-licensemacro-1151450.patch
Patch3015: vim-7.4-ssh-keywords.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel python3-devel ncurses-devel gettext perl-devel
BuildRequires: perl(ExtUtils::Embed) perl(ExtUtils::ParseXS)
BuildRequires: libacl-devel gpm-devel autoconf
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
%if "%{withruby}" == "1"
Buildrequires: ruby-devel ruby
%endif
%if "%{withlua}" == "1"
Buildrequires: lua-devel
%endif
%if %{desktop_file}
# for /usr/bin/desktop-file-install
Requires: desktop-file-utils
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
%endif
Epoch: 2
Conflicts: filesystem < 3

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor
Group: Applications/Editors
Conflicts: man-pages-fr < 0.9.7-14
Conflicts: man-pages-it < 0.3.0-17
Conflicts: man-pages-pl < 0.24-2
Requires: %{name}-filesystem

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.

%package spell
Summary: The dictionaries for spell checking. This package is optional
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release}

%description spell
This subpackage contains dictionaries for vim spell checking in
many different languages.

%package minimal
Summary: A minimal version of the VIM editor
Group: Applications/Editors
Provides: vi = %{version}-%{release}
Provides: /bin/vi

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.

%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} which
Provides: vim = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.

%package filesystem
Summary: VIM filesystem layout
Group: Applications/Editors

%Description filesystem
This package provides some directories which are required by other
packages that add vim files, p.e.  additional syntax files or filetypes.

%package X11
Summary: The VIM version of the vi editor for the X Window System
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} libattr >= 2.4 gtk2 >= 2.6
Provides: gvim = %{version}-%{release}
BuildRequires: gtk2-devel libSM-devel libXt-devel libXpm-devel
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: hicolor-icon-theme

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.

%prep
%setup -q -b 0 -n %{vimdir}
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
%patch2002 -p1
%patch2003 -p1
%if %{withhunspell}
%patch2011 -p1
%endif
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

# Base patches...
%patch001 -p0
%patch002 -p0
%patch003 -p0
%patch004 -p0
%patch005 -p0
%patch006 -p0
%patch007 -p0
%patch008 -p0
%patch009 -p0
%patch010 -p0
%patch011 -p0
%patch012 -p0
%patch013 -p0
%patch014 -p0
%patch015 -p0
%patch016 -p0
%patch017 -p0
%patch018 -p0
%patch019 -p0
%patch020 -p0
%patch021 -p0
%patch022 -p0
%patch023 -p0
%patch024 -p0
%patch025 -p0
%patch026 -p0
%patch027 -p0
%patch028 -p0
%patch029 -p0
%patch030 -p0
%patch031 -p0
%patch032 -p0
%patch033 -p0
%patch034 -p0
%patch035 -p0
%patch036 -p0
%patch037 -p0
%patch038 -p0
%patch039 -p0
%patch040 -p0
%patch041 -p0
%patch042 -p0
%patch043 -p0
%patch044 -p0
%patch045 -p0
%patch046 -p0
%patch047 -p0
%patch048 -p0
%patch049 -p0
%patch050 -p0
%patch051 -p0
%patch052 -p0
%patch053 -p0
%patch054 -p0
%patch055 -p0
%patch056 -p0
%patch057 -p0
%patch058 -p0
%patch059 -p0
%patch060 -p0
%patch061 -p0
%patch062 -p0
%patch063 -p0
%patch064 -p0
%patch065 -p0
%patch066 -p0
%patch067 -p0
%patch068 -p0
%patch069 -p0
%patch070 -p0
%patch071 -p0
%patch072 -p0
%patch073 -p0
%patch074 -p0
%patch075 -p0
%patch076 -p0
%patch077 -p0
%patch078 -p0
%patch079 -p0
%patch080 -p0
%patch081 -p0
%patch082 -p0
%patch083 -p0
%patch084 -p0
%patch085 -p0
%patch086 -p0
%patch087 -p0
%patch088 -p0
%patch089 -p0
%patch090 -p0
%patch091 -p0
%patch092 -p0
%patch093 -p0
%patch094 -p0
%patch095 -p0
%patch096 -p0
%patch097 -p0
%patch098 -p0
%patch099 -p0
%patch100 -p0
%patch101 -p0
%patch102 -p0
%patch103 -p0
%patch104 -p0
%patch105 -p0
%patch106 -p0
%patch107 -p0
%patch108 -p0
%patch109 -p0
%patch110 -p0
%patch111 -p0
%patch112 -p0
%patch113 -p0
%patch114 -p0
%patch115 -p0
%patch116 -p0
%patch117 -p0
%patch118 -p0
%patch119 -p0
%patch120 -p0
%patch121 -p0
%patch122 -p0
%patch123 -p0
%patch124 -p0
%patch125 -p0
%patch126 -p0
%patch127 -p0
%patch128 -p0
%patch129 -p0
%patch130 -p0
%patch131 -p0
%patch132 -p0
%patch133 -p0
%patch134 -p0
%patch135 -p0
%patch136 -p0
%patch137 -p0
%patch138 -p0
%patch139 -p0
%patch140 -p0
%patch141 -p0
%patch142 -p0
%patch143 -p0
%patch144 -p0
%patch145 -p0
%patch146 -p0
%patch147 -p0
%patch148 -p0
%patch149 -p0
%patch150 -p0
%patch151 -p0
%patch152 -p0
%patch153 -p0
%patch154 -p0
%patch155 -p0
%patch156 -p0
%patch157 -p0
%patch158 -p0
%patch159 -p0
%patch160 -p0
%patch161 -p0
%patch162 -p0
%patch163 -p0
%patch164 -p0
%patch165 -p0
%patch166 -p0
%patch167 -p0
%patch168 -p0
%patch169 -p0
%patch170 -p0
%patch171 -p0
%patch172 -p0
%patch173 -p0
%patch174 -p0
%patch175 -p0
%patch176 -p0
%patch177 -p0
%patch178 -p0
%patch179 -p0
%patch180 -p0
%patch181 -p0
%patch182 -p0
%patch183 -p0
%patch184 -p0
%patch185 -p0
%patch186 -p0
%patch187 -p0
%patch188 -p0
%patch189 -p0
%patch190 -p0
%patch191 -p0
%patch192 -p0
%patch193 -p0
%patch194 -p0
%patch195 -p0
%patch196 -p0
%patch197 -p0
%patch198 -p0
%patch199 -p0
%patch200 -p0
%patch201 -p0
%patch202 -p0
%patch203 -p0
%patch204 -p0
%patch205 -p0
%patch206 -p0
%patch207 -p0
#patch208 -p0
%patch209 -p0
%patch210 -p0
%patch211 -p0
%patch212 -p0
%patch213 -p0
%patch214 -p0
%patch215 -p0
%patch216 -p0
%patch217 -p0
%patch218 -p0
%patch219 -p0
%patch220 -p0
%patch221 -p0
%patch222 -p0
%patch223 -p0
%patch224 -p0
%patch225 -p0
%patch226 -p0
%patch227 -p0
%patch228 -p0
%patch229 -p0
%patch230 -p0
%patch231 -p0
%patch232 -p0
%patch233 -p0
%patch234 -p0
%patch235 -p0
%patch236 -p0
%patch237 -p0
%patch238 -p0
%patch239 -p0
%patch240 -p0
%patch241 -p0
%patch242 -p0
%patch243 -p0
%patch244 -p0
%patch245 -p0
%patch246 -p0
%patch247 -p0
%patch248 -p0
%patch249 -p0
%patch250 -p0
%patch251 -p0
%patch252 -p0
%patch253 -p0
%patch254 -p0
%patch255 -p0
%patch256 -p0
%patch257 -p0
%patch258 -p0
%patch259 -p0
%patch260 -p0
%patch261 -p0
%patch262 -p0
%patch263 -p0
%patch264 -p0
%patch265 -p0
%patch266 -p0
%patch267 -p0
%patch268 -p0
%patch269 -p0
%patch270 -p0
%patch271 -p0
%patch272 -p0
%patch273 -p0
%patch274 -p0
%patch275 -p0
%patch276 -p0
%patch277 -p0
%patch278 -p0
%patch279 -p0
%patch280 -p0
%patch281 -p0
%patch282 -p0
%patch283 -p0
%patch284 -p0
%patch285 -p0
%patch286 -p0
%patch287 -p0
%patch288 -p0
%patch289 -p0
%patch290 -p0
%patch291 -p0
%patch292 -p0
%patch293 -p0
%patch294 -p0
%patch295 -p0
%patch296 -p0
%patch297 -p0
%patch298 -p0
%patch299 -p0
%patch300 -p0
%patch301 -p0
%patch302 -p0
%patch303 -p0
%patch304 -p0
%patch305 -p0
%patch306 -p0
%patch307 -p0
%patch308 -p0
%patch309 -p0
%patch310 -p0
%patch311 -p0
%patch312 -p0
%patch313 -p0
%patch314 -p0
%patch315 -p0
%patch316 -p0
%patch317 -p0
%patch318 -p0
%patch319 -p0
%patch320 -p0
%patch321 -p0
%patch322 -p0
%patch323 -p0
%patch324 -p0
%patch325 -p0
%patch326 -p0
%patch327 -p0
%patch328 -p0
%patch329 -p0
%patch330 -p0
%patch331 -p0
%patch332 -p0
%patch333 -p0
%patch334 -p0
%patch335 -p0
%patch336 -p0
%patch337 -p0
%patch338 -p0
%patch339 -p0
%patch340 -p0
%patch341 -p0
%patch342 -p0
%patch343 -p0
%patch344 -p0
%patch345 -p0
%patch346 -p0
%patch347 -p0
%patch348 -p0
%patch349 -p0
%patch350 -p0
%patch351 -p0
%patch352 -p0
%patch353 -p0
%patch354 -p0
%patch355 -p0
%patch356 -p0
%patch357 -p0
%patch358 -p0
%patch359 -p0
%patch360 -p0
%patch361 -p0
%patch362 -p0
%patch363 -p0
%patch364 -p0
%patch365 -p0
%patch366 -p0
%patch367 -p0
%patch368 -p0
%patch369 -p0
%patch370 -p0
%patch371 -p0
%patch372 -p0
%patch373 -p0
%patch374 -p0
%patch375 -p0
%patch376 -p0
%patch377 -p0
%patch378 -p0
%patch379 -p0
%patch380 -p0
%patch381 -p0
%patch382 -p0
%patch383 -p0
%patch384 -p0
%patch385 -p0
%patch386 -p0
%patch387 -p0
%patch388 -p0
%patch389 -p0
%patch390 -p0
%patch391 -p0
%patch392 -p0
%patch393 -p0
%patch394 -p0
%patch395 -p0
%patch396 -p0
%patch397 -p0
%patch398 -p0
%patch399 -p0
%patch400 -p0
%patch401 -p0
%patch402 -p0
%patch403 -p0
%patch404 -p0
%patch405 -p0
%patch406 -p0
%patch407 -p0
%patch408 -p0
%patch409 -p0
%patch410 -p0
%patch411 -p0
%patch412 -p0
%patch413 -p0
%patch414 -p0
%patch415 -p0
%patch416 -p0
%patch417 -p0
%patch418 -p0
%patch419 -p0
%patch420 -p0
%patch421 -p0
%patch422 -p0
%patch423 -p0
%patch424 -p0
%patch425 -p0
%patch426 -p0
%patch427 -p0
%patch428 -p0
%patch429 -p0
%patch430 -p0
%patch431 -p0
%patch432 -p0
%patch433 -p0
%patch434 -p0
%patch435 -p0
%patch436 -p0
%patch437 -p0
%patch438 -p0
%patch439 -p0
%patch440 -p0
%patch441 -p0
%patch442 -p0
%patch443 -p0
%patch444 -p0
%patch445 -p0
%patch446 -p0
%patch447 -p0
%patch448 -p0
%patch449 -p0
%patch450 -p0
%patch451 -p0
%patch452 -p0
%patch453 -p0
%patch454 -p0
%patch455 -p0
%patch456 -p0
%patch457 -p0
%patch458 -p0
%patch459 -p0
%patch460 -p0
%patch461 -p0
%patch462 -p0
%patch463 -p0
%patch464 -p0
%patch465 -p0
%patch466 -p0
%patch467 -p0
%patch468 -p0
%patch469 -p0
%patch470 -p0
%patch471 -p0
%patch472 -p0
%patch473 -p0
%patch474 -p0
%patch475 -p0
%patch476 -p0
%patch477 -p0
%patch478 -p0
%patch479 -p0
%patch480 -p0
%patch481 -p0
%patch482 -p0
%patch483 -p0
%patch484 -p0
%patch485 -p0
%patch486 -p0
%patch487 -p0
%patch488 -p0
%patch489 -p0
%patch490 -p0
%patch491 -p0
%patch492 -p0
%patch493 -p0
%patch494 -p0
%patch495 -p0
%patch496 -p0
%patch497 -p0
%patch498 -p0
%patch499 -p0
%patch500 -p0
%patch501 -p0
%patch502 -p0
%patch503 -p0
%patch504 -p0
%patch505 -p0
%patch506 -p0
%patch507 -p0
%patch508 -p0
%patch509 -p0
%patch510 -p0
%patch511 -p0
%patch512 -p0
%patch513 -p0
%patch514 -p0
%patch515 -p0
%patch516 -p0
%patch517 -p0
%patch518 -p0
%patch519 -p0
%patch520 -p0
%patch521 -p0
%patch522 -p0
%patch523 -p0
%patch524 -p0
%patch525 -p0
%patch526 -p0
%patch527 -p0
%patch528 -p0
%patch529 -p0
%patch530 -p0
%patch531 -p0
%patch532 -p0
%patch533 -p0
%patch534 -p0
%patch535 -p0
%patch536 -p0
%patch537 -p0
%patch538 -p0
%patch539 -p0
%patch540 -p0
%patch541 -p0
%patch542 -p0
%patch543 -p0
%patch544 -p0
%patch545 -p0
%patch546 -p0
%patch547 -p0
%patch548 -p0
%patch549 -p0
%patch550 -p0
%patch551 -p0
%patch552 -p0
%patch553 -p0
%patch554 -p0
%patch555 -p0
%patch556 -p0
%patch557 -p0
%patch558 -p0
%patch559 -p0
%patch1559 -p0
%patch560 -p0
%patch561 -p0
%patch562 -p0
%patch563 -p0
%patch564 -p0
%patch565 -p0
%patch566 -p0
%patch567 -p0
%patch568 -p0
%patch569 -p0
%patch570 -p0
%patch571 -p0
%patch572 -p0
%patch573 -p0
%patch574 -p0
%patch575 -p0
%patch576 -p0
%patch577 -p0
%patch578 -p0
%patch579 -p0
%patch580 -p0
%patch581 -p0
%patch582 -p0
%patch583 -p0
%patch584 -p0
%patch585 -p0
%patch586 -p0
%patch587 -p0
%patch588 -p0
%patch589 -p0
%patch590 -p0
%patch591 -p0
%patch592 -p0
%patch593 -p0
%patch594 -p0
%patch595 -p0
%patch596 -p0
%patch597 -p0
%patch598 -p0
%patch599 -p0
%patch600 -p0
%patch601 -p0
%patch602 -p0
%patch603 -p0
%patch604 -p0
%patch605 -p0
%patch606 -p0
%patch607 -p0
%patch608 -p0
%patch609 -p0
%patch610 -p0
%patch611 -p0
%patch612 -p0
%patch613 -p0
%patch614 -p0
%patch615 -p0
%patch616 -p0
%patch617 -p0
%patch618 -p0
%patch619 -p0
%patch620 -p0
%patch621 -p0
%patch622 -p0
%patch623 -p0
%patch624 -p0
%patch625 -p0
%patch626 -p0
%patch627 -p0
%patch628 -p0
%patch629 -p0
%patch630 -p0
%patch631 -p0
%patch632 -p0
%patch633 -p0
%patch634 -p0
%patch635 -p0
%patch636 -p0
%patch637 -p0
%patch638 -p0
%patch639 -p0
%patch640 -p0
%patch641 -p0
%patch642 -p0
%patch643 -p0
%patch644 -p0
%patch645 -p0
%patch646 -p0
%patch647 -p0
%patch648 -p0
%patch649 -p0
%patch650 -p0
%patch651 -p0
%patch652 -p0
%patch653 -p0
%patch654 -p0
%patch655 -p0
%patch656 -p0
%patch657 -p0
%patch658 -p0
%patch659 -p0
%patch660 -p0
%patch661 -p0
%patch662 -p0
%patch663 -p0
%patch664 -p0
%patch665 -p0
%patch666 -p0
%patch667 -p0
%patch668 -p0
%patch669 -p0
%patch670 -p0
%patch671 -p0
%patch672 -p0
%patch673 -p0
%patch674 -p0
%patch675 -p0
%patch676 -p0
%patch677 -p0
%patch678 -p0
%patch679 -p0
%patch680 -p0
%patch681 -p0
%patch682 -p0
%patch683 -p0
%patch684 -p0
%patch685 -p0
%patch686 -p0
%patch687 -p0
%patch688 -p0
%patch689 -p0
%patch690 -p0
%patch691 -p0
%patch692 -p0
%patch693 -p0
%patch694 -p0
%patch695 -p0
%patch696 -p0
%patch697 -p0
%patch698 -p0
%patch699 -p0
%patch700 -p0
%patch701 -p0
%patch702 -p0
%patch703 -p0
%patch704 -p0
%patch705 -p0
%patch706 -p0
%patch707 -p0
%patch708 -p0
%patch709 -p0
%patch710 -p0
%patch711 -p0
%patch712 -p0
%patch713 -p0
%patch714 -p0
%patch715 -p0
%patch716 -p0
%patch717 -p0
%patch718 -p0
%patch719 -p0
%patch720 -p0
%patch721 -p0
%patch722 -p0
%patch723 -p0
%patch724 -p0
%patch725 -p0
%patch726 -p0
%patch727 -p0
%patch728 -p0

# install spell files
%if %{withvimspell}
%{__tar} xjf %{SOURCE13}
%endif

%patch3000 -p1
%patch3002 -p1
%patch3004 -p1
%patch3006 -p1
%patch3007 -p1
%patch3008 -p1
%patch3009 -p1
%patch3010 -p1
%patch3011 -p1
%patch3012 -p1

%patch3013 -p1
%patch3015 -p1

%build
cp -f %{SOURCE5} .
cd src
autoconf

sed -i 's|VIMRCLOC	= \$(VIMLOC)|VIMRCLOC	= /etc|' Makefile

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"

cp -f os_unix.h os_unix.h.save
cp -f ex_cmds.c ex_cmds.c.save

perl -pi -e "s/help.txt/vi_help.txt/"  os_unix.h ex_cmds.c
perl -pi -e "s/\/etc\/vimrc/\/etc\/virc/"  os_unix.h
%configure --prefix=%{_prefix} --with-features=small --with-x=no \
  --enable-multibyte \
  --disable-netbeans \
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
  --disable-pythoninterp --disable-perlinterp --disable-tclinterp \
  --with-tlib=ncurses --enable-gui=no --disable-gpm --exec-prefix=/ \
  --with-compiledby="<bugzilla@redhat.com>" \
  --with-modified-by="<bugzilla@redhat.com>"

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim minimal-vim
make clean

mv -f os_unix.h.save os_unix.h
mv -f ex_cmds.c.save ex_cmds.c

%configure --with-features=huge \
  --enable-pythoninterp=dynamic \
  --enable-python3interp=dynamic \
  --enable-perlinterp \
  --disable-tclinterp --with-x=yes \
  --enable-xim --enable-multibyte \
  --with-tlib=ncurses \
  --enable-fontset --enable-sniff \
  --enable-gtk2-check --enable-gui=gtk2 \
  --with-compiledby="<bugzilla@redhat.com>" --enable-cscope \
  --with-modified-by="<bugzilla@redhat.com>" \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp=dynamic \
%else
  --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
  --enable-luainterp \
%else
  --disable-luainterp \
%endif

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim gvim
make clean

%configure --prefix=%{_prefix} --with-features=huge \
 --enable-pythoninterp=dynamic \
 --enable-python3interp=dynamic \
 --enable-perlinterp \
 --disable-tclinterp \
 --with-x=yes \
 --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
 --with-tlib=ncurses \
 --enable-sniff \
 --with-compiledby="<bugzilla@redhat.com>" --enable-cscope \
 --with-modified-by="<bugzilla@redhat.com>" \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp=dynamic \
%else
  --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
  --enable-luainterp \
%else
  --disable-luainterp \
%endif

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim enhanced-vim

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/%{name}/vimfiles/{after,autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
mkdir -p %{buildroot}/%{_datadir}/%{name}/vimfiles/after/{autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
cp -f %{SOURCE11} .
%if %{?fedora}%{!?fedora:0} >= 16 || %{?rhel}%{!?rhel:0} >= 6
cp -f %{SOURCE15} %{buildroot}/%{_datadir}/%{name}/vimfiles/template.spec
%else
cp -f %{SOURCE14} %{buildroot}/%{_datadir}/%{name}/vimfiles/template.spec
%endif
cp runtime/doc/uganda.txt LICENSE
# Those aren't Linux info files but some binary files for Amiga:
rm -f README*.info


cd src
make install DESTDIR=%{buildroot} BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
make installgtutorbin  DESTDIR=%{buildroot} BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m755 minimal-vim %{buildroot}%{_bindir}/vi
install -m755 enhanced-vim %{buildroot}%{_bindir}/vim
install -m755 gvim %{buildroot}%{_bindir}/gvim
install -p -m644 %{SOURCE7} \
   %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/gvim.png
install -p -m644 %{SOURCE8} \
   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/gvim.png
install -p -m644 %{SOURCE9} \
   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/gvim.png
install -p -m644 %{SOURCE10} \
   %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/gvim.png

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/gvim.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
EmailAddress: Bram@moolenaar.net>
SentUpstream: 2014-05-22
-->
<application>
  <id type="desktop">gvim.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>Vim</project_license>
  <description>
    <p>
     Vim is an advanced text editor that seeks to provide the power of the
     de-facto Unix editor 'Vi', with a more complete feature set.
     It's useful whether you're already using vi or using a different editor.
    </p>
    <p>
     Vim is a highly configurable text editor built to enable efficient text
     editing.
     Vim is often called a "programmer's editor," and so useful for programming
     that many consider it an entire IDE. It's not just for programmers, though.
     Vim is perfect for all kinds of text editing, from composing email to
     editing configuration files.
    </p>
  </description>
  <url type="homepage">http://www.vim.org/</url>
</application>
EOF

( cd %{buildroot}
  ln -sf vi ./%{_bindir}/rvi
  ln -sf vi ./%{_bindir}/rview
  ln -sf vi ./%{_bindir}/view
  ln -sf vi ./%{_bindir}/ex
  ln -sf vim ./%{_bindir}/rvim
  ln -sf vim ./%{_bindir}/vimdiff
  perl -pi -e "s,%{buildroot},," .%{_mandir}/man1/vim.1 .%{_mandir}/man1/vimtutor.1
  rm -f .%{_mandir}/man1/rvim.1
  ln -sf vim.1.gz .%{_mandir}/man1/vi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/rvi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/vimdiff.1.gz
  ln -sf gvim ./%{_bindir}/gview
  ln -sf gvim ./%{_bindir}/gex
  ln -sf gvim ./%{_bindir}/evim
  ln -sf gvim ./%{_bindir}/gvimdiff
  ln -sf gvim ./%{_bindir}/vimx
  %if "%{desktop_file}" == "1"
    mkdir -p %{buildroot}/%{_datadir}/applications
    desktop-file-install \
    %if 0%{?fedora} && 0%{?fedora} < 19
        --vendor fedora \
    %endif
        --dir %{buildroot}/%{_datadir}/applications \
        %{SOURCE3}
        # --add-category "Development;TextEditor;X-Red-Hat-Base" D\
  %else
    mkdir -p ./%{_sysconfdir}/X11/applnk/Applications
    cp %{SOURCE3} ./%{_sysconfdir}/X11/applnk/Applications/gvim.desktop
  %endif
  # ja_JP.ujis is obsolete, ja_JP.eucJP is recommended.
  ( cd ./%{_datadir}/%{name}/%{vimdir}/lang; \
    ln -sf menu_ja_jp.ujis.vim menu_ja_jp.eucjp.vim )
)

pushd %{buildroot}/%{_datadir}/%{name}/%{vimdir}/tutor
mkdir conv
   iconv -f CP1252 -t UTF8 tutor.ca > conv/tutor.ca
   iconv -f CP1252 -t UTF8 tutor.it > conv/tutor.it
   #iconv -f CP1253 -t UTF8 tutor.gr > conv/tutor.gr
   iconv -f CP1252 -t UTF8 tutor.fr > conv/tutor.fr
   iconv -f CP1252 -t UTF8 tutor.es > conv/tutor.es
   iconv -f CP1252 -t UTF8 tutor.de > conv/tutor.de
   #iconv -f CP737 -t UTF8 tutor.gr.cp737 > conv/tutor.gr.cp737
   #iconv -f EUC-JP -t UTF8 tutor.ja.euc > conv/tutor.ja.euc
   #iconv -f SJIS -t UTF8 tutor.ja.sjis > conv/tutor.ja.sjis
   iconv -f UTF8 -t UTF8 tutor.ja.utf-8 > conv/tutor.ja.utf-8
   iconv -f UTF8 -t UTF8 tutor.ko.utf-8 > conv/tutor.ko.utf-8
   iconv -f CP1252 -t UTF8 tutor.no > conv/tutor.no
   iconv -f ISO-8859-2 -t UTF8 tutor.pl > conv/tutor.pl
   iconv -f ISO-8859-2 -t UTF8 tutor.sk > conv/tutor.sk
   iconv -f KOI8R -t UTF8 tutor.ru > conv/tutor.ru
   iconv -f CP1252 -t UTF8 tutor.sv > conv/tutor.sv
   mv -f tutor.ja.euc tutor.ja.sjis tutor.ko.euc tutor.pl.cp1250 tutor.zh.big5 tutor.ru.cp1251 tutor.zh.euc conv/
   rm -f tutor.ca tutor.de tutor.es tutor.fr tutor.gr tutor.it tutor.ja.utf-8 tutor.ko.utf-8 tutor.no tutor.pl tutor.sk tutor.ru tutor.sv
mv -f conv/* .
rmdir conv
popd

# Dependency cleanups
chmod 644 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/doc/vim2html.pl \
 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/tools/*.pl \
 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/tools/vim132
chmod 644 ../runtime/doc/vim2html.pl

mkdir -p %{buildroot}/%{_sysconfdir}/profile.d
cat >%{buildroot}/%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
  [ -x %{_bindir}/id ] || return
  ID=\`/usr/bin/id -u\`
  [ -n "\$ID" -a "\$ID" -le 200 ] && return
  # for bash and zsh, only if no alias is already set
  alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >%{buildroot}/%{_sysconfdir}/profile.d/vim.csh <<EOF
if ( -x /usr/bin/id ) then
    if ( "\`/usr/bin/id -u\`" > 200 ) then
        alias vi vim
    endif
endif
EOF
chmod 0644 %{buildroot}/%{_sysconfdir}/profile.d/*
install -p -m644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/vimrc
install -p -m644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/virc
(cd %{buildroot}/%{_datadir}/%{name}/%{vimdir}/doc;
 gzip -9 *.txt
 gzip -d help.txt.gz version7.txt.gz sponsor.txt.gz
 cp %{SOURCE12} .
 cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/;s/\tversion7.txt.gz\t/\tversion7.txt\t/;s/\tsponsor.txt.gz\t/\tsponsor.txt\t/' > tags.new; mv -f tags.new tags
cat >> tags << EOF
vi_help.txt	vi_help.txt	/*vi_help.txt*
vi-author.txt	vi_help.txt	/*vi-author*
vi-Bram.txt	vi_help.txt	/*vi-Bram*
vi-Moolenaar.txt	vi_help.txt	/*vi-Moolenaar*
vi-credits.txt	vi_help.txt	/*vi-credits*
EOF
LANG=C sort tags > tags.tmp; mv tags.tmp tags
 )
(cd ../runtime; rm -rf doc; ln -svf ../../vim/%{vimdir}/doc docs;)
rm -f %{buildroot}/%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf %{buildroot}/%{_datadir}/vim/%{vimdir}/tools
rm -rf %{buildroot}/%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f %{buildroot}/%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~
( cd %{buildroot}/%{_mandir}
  for i in `find ??/ -type f`; do
    bi=`basename $i`
    iconv -f latin1 -t UTF8 $i > %{buildroot}/$bi
    mv -f %{buildroot}/$bi $i
  done
)

# Remove not UTF-8 manpages
for i in pl.ISO8859-2 it.ISO8859-1 ru.KOI8-R fr.ISO8859-1; do
  rm -rf %{buildroot}/%{_mandir}/$i
done

# use common man1/ru directory
mv %{buildroot}/%{_mandir}/ru.UTF-8 %{buildroot}/%{_mandir}/ru

# Remove duplicate man pages
for i in fr.UTF-8 it.UTF-8 pl.UTF-8; do
  rm -rf %{buildroot}/%{_mandir}/$i
done

for i in rvim.1 gvim.1 gex.1 gview.1 vimx.1; do
  echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man1/$i
done
echo ".so man1/vimdiff.1" > %{buildroot}/%{_mandir}/man1/gvimdiff.1
echo ".so man1/vimtutor.1" > %{buildroot}/%{_mandir}/man1/gvimtutor.1
mkdir -p %{buildroot}/%{_mandir}/man5
for i in virc.5 vimrc.5; do
  echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man5/$i
done
touch %{buildroot}/%{_datadir}/%{name}/vimfiles/doc/tags

%post X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /%{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi
update-desktop-database &> /dev/null ||:

%postun X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /%{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi
update-desktop-database &> /dev/null ||:

%clean
rm -rf %{buildroot}

%files common
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/vimrc
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README*
%doc runtime/docs
%doc Changelog.rpm
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/vimfiles/template.spec
%dir %{_datadir}/%{name}/%{vimdir}
%{_datadir}/%{name}/%{vimdir}/autoload
%{_datadir}/%{name}/%{vimdir}/colors
%{_datadir}/%{name}/%{vimdir}/compiler
%{_datadir}/%{name}/%{vimdir}/doc
%{_datadir}/%{name}/%{vimdir}/*.vim
%{_datadir}/%{name}/%{vimdir}/ftplugin
%{_datadir}/%{name}/%{vimdir}/indent
%{_datadir}/%{name}/%{vimdir}/keymap
%{_datadir}/%{name}/%{vimdir}/lang/*.vim
%{_datadir}/%{name}/%{vimdir}/lang/*.txt
%dir %{_datadir}/%{name}/%{vimdir}/lang
%{_datadir}/%{name}/%{vimdir}/macros
%{_datadir}/%{name}/%{vimdir}/plugin
%{_datadir}/%{name}/%{vimdir}/print
%{_datadir}/%{name}/%{vimdir}/syntax
%{_datadir}/%{name}/%{vimdir}/tutor
%if ! %{withvimspell}
%{_datadir}/%{name}/%{vimdir}/spell
%endif
%lang(af) %{_datadir}/%{name}/%{vimdir}/lang/af
%lang(ca) %{_datadir}/%{name}/%{vimdir}/lang/ca
%lang(cs) %{_datadir}/%{name}/%{vimdir}/lang/cs
%lang(cs.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/cs.cp1250
%lang(de) %{_datadir}/%{name}/%{vimdir}/lang/de
%lang(en_GB) %{_datadir}/%{name}/%{vimdir}/lang/en_GB
%lang(eo) %{_datadir}/%{name}/%{vimdir}/lang/eo
%lang(es) %{_datadir}/%{name}/%{vimdir}/lang/es
%lang(fi) %{_datadir}/%{name}/%{vimdir}/lang/fi
%lang(fr) %{_datadir}/%{name}/%{vimdir}/lang/fr
%lang(ga) %{_datadir}/%{name}/%{vimdir}/lang/ga
%lang(it) %{_datadir}/%{name}/%{vimdir}/lang/it
%lang(ja) %{_datadir}/%{name}/%{vimdir}/lang/ja
%lang(ja.euc-jp) %{_datadir}/%{name}/%{vimdir}/lang/ja.euc-jp
%lang(ja.sjis) %{_datadir}/%{name}/%{vimdir}/lang/ja.sjis
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko.UTF-8
%lang(nb) %{_datadir}/%{name}/%{vimdir}/lang/nb
%lang(nl) %{_datadir}/%{name}/%{vimdir}/lang/nl
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/no
%lang(pl) %{_datadir}/%{name}/%{vimdir}/lang/pl
%lang(pl.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/pl.UTF-8
%lang(pl.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/pl.cp1250
%lang(pt_BR) %{_datadir}/%{name}/%{vimdir}/lang/pt_BR
%lang(ru) %{_datadir}/%{name}/%{vimdir}/lang/ru
%lang(ru.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/ru.cp1251
%lang(sk) %{_datadir}/%{name}/%{vimdir}/lang/sk
%lang(sk.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/sk.cp1250
%lang(sv) %{_datadir}/%{name}/%{vimdir}/lang/sv
%lang(uk) %{_datadir}/%{name}/%{vimdir}/lang/uk
%lang(uk.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/uk.cp1251
%lang(vi) %{_datadir}/%{name}/%{vimdir}/lang/vi
%lang(zh_CN) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN
%lang(zh_CN.cp936) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.cp936
%lang(zh_TW) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW.UTF-8
/%{_bindir}/xxd
%{_mandir}/man1/ex.*
%{_mandir}/man1/gex.*
%{_mandir}/man1/gview.*
%{_mandir}/man1/gvim*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/rvim.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/view.*
%{_mandir}/man1/vim.*
%{_mandir}/man1/vimdiff.*
%{_mandir}/man1/vimtutor.*
%{_mandir}/man1/vimx.*
%{_mandir}/man1/xxd.*
%{_mandir}/man5/vimrc.*
%lang(fr) %{_mandir}/fr/man1/*
%lang(it) %{_mandir}/it/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(ru) %{_mandir}/ru/man1/*

%if %{withvimspell}
%files spell
%defattr(-,root,root)
%dir %{_datadir}/%{name}/%{vimdir}/spell
%{_datadir}/%{name}/vim70/spell/cleanadd.vim
%lang(af) %{_datadir}/%{name}/%{vimdir}/spell/af.*
%lang(am) %{_datadir}/%{name}/%{vimdir}/spell/am.*
%lang(bg) %{_datadir}/%{name}/%{vimdir}/spell/bg.*
%lang(ca) %{_datadir}/%{name}/%{vimdir}/spell/ca.*
%lang(cs) %{_datadir}/%{name}/%{vimdir}/spell/cs.*
%lang(cy) %{_datadir}/%{name}/%{vimdir}/spell/cy.*
%lang(da) %{_datadir}/%{name}/%{vimdir}/spell/da.*
%lang(de) %{_datadir}/%{name}/%{vimdir}/spell/de.*
%lang(el) %{_datadir}/%{name}/%{vimdir}/spell/el.*
%lang(en) %{_datadir}/%{name}/%{vimdir}/spell/en.*
%lang(eo) %{_datadir}/%{name}/%{vimdir}/spell/eo.*
%lang(es) %{_datadir}/%{name}/%{vimdir}/spell/es.*
%lang(fo) %{_datadir}/%{name}/%{vimdir}/spell/fo.*
%lang(fr) %{_datadir}/%{name}/%{vimdir}/spell/fr.*
%lang(ga) %{_datadir}/%{name}/%{vimdir}/spell/ga.*
%lang(gd) %{_datadir}/%{name}/%{vimdir}/spell/gd.*
%lang(gl) %{_datadir}/%{name}/%{vimdir}/spell/gl.*
%lang(he) %{_datadir}/%{name}/%{vimdir}/spell/he.*
%lang(hr) %{_datadir}/%{name}/%{vimdir}/spell/hr.*
%lang(hu) %{_datadir}/%{name}/%{vimdir}/spell/hu.*
%lang(id) %{_datadir}/%{name}/%{vimdir}/spell/id.*
%lang(it) %{_datadir}/%{name}/%{vimdir}/spell/it.*
%lang(ku) %{_datadir}/%{name}/%{vimdir}/spell/ku.*
%lang(la) %{_datadir}/%{name}/%{vimdir}/spell/la.*
%lang(lt) %{_datadir}/%{name}/%{vimdir}/spell/lt.*
%lang(lv) %{_datadir}/%{name}/%{vimdir}/spell/lv.*
%lang(mg) %{_datadir}/%{name}/%{vimdir}/spell/mg.*
%lang(mi) %{_datadir}/%{name}/%{vimdir}/spell/mi.*
%lang(ms) %{_datadir}/%{name}/%{vimdir}/spell/ms.*
%lang(nb) %{_datadir}/%{name}/%{vimdir}/spell/nb.*
%lang(nl) %{_datadir}/%{name}/%{vimdir}/spell/nl.*
%lang(nn) %{_datadir}/%{name}/%{vimdir}/spell/nn.*
%lang(ny) %{_datadir}/%{name}/%{vimdir}/spell/ny.*
%lang(pl) %{_datadir}/%{name}/%{vimdir}/spell/pl.*
%lang(pt) %{_datadir}/%{name}/%{vimdir}/spell/pt.*
%lang(ro) %{_datadir}/%{name}/%{vimdir}/spell/ro.*
%lang(ru) %{_datadir}/%{name}/%{vimdir}/spell/ru.*
%lang(rw) %{_datadir}/%{name}/%{vimdir}/spell/rw.*
%lang(sk) %{_datadir}/%{name}/%{vimdir}/spell/sk.*
%lang(sl) %{_datadir}/%{name}/%{vimdir}/spell/sl.*
%lang(sv) %{_datadir}/%{name}/%{vimdir}/spell/sv.*
%lang(sw) %{_datadir}/%{name}/%{vimdir}/spell/sw.*
%lang(tet) %{_datadir}/%{name}/%{vimdir}/spell/tet.*
%lang(th) %{_datadir}/%{name}/%{vimdir}/spell/th.*
%lang(tl) %{_datadir}/%{name}/%{vimdir}/spell/tl.*
%lang(tn) %{_datadir}/%{name}/%{vimdir}/spell/tn.*
%lang(uk) %{_datadir}/%{name}/%{vimdir}/spell/uk.*
%lang(yi) %{_datadir}/%{name}/%{vimdir}/spell/yi.*
%lang(yi-tr) %{_datadir}/%{name}/%{vimdir}/spell/yi-tr.*
%lang(zu) %{_datadir}/%{name}/%{vimdir}/spell/zu.*
%endif

%files minimal
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/virc
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvi
%{_bindir}/rview
%{_mandir}/man1/vim.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/view.*
%{_mandir}/man5/virc.*

%files enhanced
%defattr(-,root,root)
%{_bindir}/vim
%{_bindir}/rvim
%{_bindir}/vimdiff
%{_bindir}/vimtutor
%config(noreplace) %{_sysconfdir}/profile.d/vim.*

%files filesystem
%defattr(-,root,root)
%dir %{_datadir}/%{name}/vimfiles
%dir %{_datadir}/%{name}/vimfiles/after
%dir %{_datadir}/%{name}/vimfiles/after/*
%dir %{_datadir}/%{name}/vimfiles/autoload
%dir %{_datadir}/%{name}/vimfiles/colors
%dir %{_datadir}/%{name}/vimfiles/compiler
%dir %{_datadir}/%{name}/vimfiles/doc
%ghost %{_datadir}/%{name}/vimfiles/doc/tags
%dir %{_datadir}/%{name}/vimfiles/ftdetect
%dir %{_datadir}/%{name}/vimfiles/ftplugin
%dir %{_datadir}/%{name}/vimfiles/indent
%dir %{_datadir}/%{name}/vimfiles/keymap
%dir %{_datadir}/%{name}/vimfiles/lang
%dir %{_datadir}/%{name}/vimfiles/plugin
%dir %{_datadir}/%{name}/vimfiles/print
%dir %{_datadir}/%{name}/vimfiles/spell
%dir %{_datadir}/%{name}/vimfiles/syntax
%dir %{_datadir}/%{name}/vimfiles/tutor

%files X11
%defattr(-,root,root)
%if "%{desktop_file}" == "1"
%{_datadir}/appdata/*.appdata.xml
/%{_datadir}/applications/*
%else
/%{_sysconfdir}/X11/applnk/*/gvim.desktop
%endif
%{_bindir}/gvimtutor
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/gview
%{_bindir}/gex
%{_bindir}/vimx
%{_bindir}/evim
%{_mandir}/man1/evim.*
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Wed May 13 2015 mosquito <sensor.wen@gmail.com> - 2:7.4.728-2
- Dynamic Lua 5.3 seems to be broken. Static seems to be okay. Lua 5.2 works fine.
  https://groups.google.com/forum/#!topic/vim_dev/UpAfD1JEaSI

* Wed May 13 2015 mosquito <sensor.wen@gmail.com> - 2:7.4.728-1
- patchlevel 728
- enable python3, lua, xfontset, sniff support

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 2:7.4.663-2
- Add an AppData file for the software center

* Sat Mar 14 2015 Karsten Hopp <karsten@redhat.com> 7.4.663-1
- patchlevel 663

* Fri Mar 13 2015 Karsten Hopp <karsten@redhat.com> 7.4.662-1
- patchlevel 662

* Sun Mar 08 2015 Karsten Hopp <karsten@redhat.com> 7.4.658-1
- patchlevel 658

* Sat Mar 07 2015 Karsten Hopp <karsten@redhat.com> 7.4.657-1
- patchlevel 657

* Fri Mar 06 2015 Karsten Hopp <karsten@redhat.com> 7.4.656-1
- patchlevel 656

* Thu Mar 05 2015 Karsten Hopp <karsten@redhat.com> 7.4.652-1
- patchlevel 652

* Sat Feb 28 2015 Karsten Hopp <karsten@redhat.com> 7.4.648-1
- patchlevel 648

* Fri Feb 27 2015 Karsten Hopp <karsten@redhat.com> 7.4.643-1
- patchlevel 643

* Fri Feb 27 2015 Dave Airlie <airlied@redhat.com> 7.4.640-4
- fix vimrc using wrong comment character

* Thu Feb 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.640-3
- bump release

* Thu Feb 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.640-2
- set background to dark in gnome-terminal, rhbz#1159920

* Wed Feb 25 2015 Karsten Hopp <karsten@redhat.com> 7.4.640-1
- patchlevel 640

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2:7.4.629-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 11 2015 Karsten Hopp <karsten@redhat.com> 7.4.629-2
- fix syntax highlighting for some ssh_config sshd_config keywords

* Wed Feb 11 2015 Karsten Hopp <karsten@redhat.com> 7.4.629-1
- patchlevel 629

* Fri Feb 06 2015 Karsten Hopp <karsten@redhat.com> 7.4.622-1
- patchlevel 622

* Thu Feb 05 2015 Karsten Hopp <karsten@redhat.com> 7.4.621-1
- patchlevel 621

* Wed Feb 04 2015 Karsten Hopp <karsten@redhat.com> 7.4.618-1
- patchlevel 618

* Tue Feb 03 2015 Karsten Hopp <karsten@redhat.com> 7.4.615-1
- patchlevel 615

* Wed Jan 28 2015 Karsten Hopp <karsten@redhat.com> 7.4.608-1
- patchlevel 608

* Tue Jan 27 2015 Karsten Hopp <karsten@redhat.com> 7.4.604-1
- patchlevel 604

* Fri Jan 23 2015 Karsten Hopp <karsten@redhat.com> 7.4.591-1
- patchlevel 591

* Wed Jan 21 2015 Karsten Hopp <karsten@redhat.com> 7.4.589-1
- patchlevel 589

* Tue Jan 20 2015 Karsten Hopp <karsten@redhat.com> 7.4.586-1
- patchlevel 586

* Sun Jan 18 2015 Karsten Hopp <karsten@redhat.com> 7.4.582-1
- patchlevel 582

* Thu Jan 15 2015 Karsten Hopp <karsten@redhat.com> 7.4.580-1
- patchlevel 580

* Wed Jan 14 2015 Karsten Hopp <karsten@redhat.com> 7.4.576-1
- patchlevel 576

* Mon Jan 12 2015 Karsten Hopp <karsten@redhat.com> 7.4.567-1
- use %%make_install in spec-template.new (rhbz#919270)

* Thu Jan 08 2015 Karsten Hopp <karsten@redhat.com> 7.4.567-1
- patchlevel 567

* Wed Jan 07 2015 Karsten Hopp <karsten@redhat.com> 7.4.566-1
- patchlevel 566

* Thu Dec 18 2014 Karsten Hopp <karsten@redhat.com> 7.4.560-1
- patchlevel 560

* Wed Dec 17 2014 Karsten Hopp <karsten@redhat.com> 7.4.557-1
- patchlevel 557

* Sun Dec 14 2014 Karsten Hopp <karsten@redhat.com> 7.4.552-1
- patchlevel 552

* Sat Dec 13 2014 Karsten Hopp <karsten@redhat.com> 7.4.546-1
- patchlevel 546

* Mon Dec 08 2014 Karsten Hopp <karsten@redhat.com> 7.4.542-1
- patchlevel 542

* Sun Dec 07 2014 Karsten Hopp <karsten@redhat.com> 7.4.541-1
- patchlevel 541

* Mon Dec 01 2014 Karsten Hopp <karsten@redhat.com> 7.4.540-1
- patchlevel 540

* Sun Nov 30 2014 Karsten Hopp <karsten@redhat.com> 7.4.539-1
- patchlevel 539

* Fri Nov 28 2014 Karsten Hopp <karsten@redhat.com> 7.4.537-1
- patchlevel 537

* Thu Nov 27 2014 Karsten Hopp <karsten@redhat.com> 7.4.534-1
- patchlevel 534

* Sun Nov 23 2014 Karsten Hopp <karsten@redhat.com> 7.4.527-1
- patchlevel 527

* Fri Nov 21 2014 Karsten Hopp <karsten@redhat.com> 7.4.526-1
- patchlevel 526

* Thu Nov 20 2014 Karsten Hopp <karsten@redhat.com> 7.4.525-1
- patchlevel 525

* Wed Nov 19 2014 Karsten Hopp <karsten@redhat.com> 7.4.521-1
- patchlevel 521

* Thu Nov 13 2014 Karsten Hopp <karsten@redhat.com> 7.4.516-1
- patchlevel 516

* Wed Nov 12 2014 Karsten Hopp <karsten@redhat.com> 7.4.512-1
- patchlevel 512

* Thu Nov 06 2014 Karsten Hopp <karsten@redhat.com> 7.4.507-1
- patchlevel 507

* Wed Nov 05 2014 Karsten Hopp <karsten@redhat.com> 7.4.502-1
- patchlevel 502

* Sat Nov 01 2014 Karsten Hopp <karsten@redhat.com> 7.4.492-1
- patchlevel 492

* Fri Oct 31 2014 Karsten Hopp <karsten@redhat.com> 7.4.491-1
- patchlevel 491

* Thu Oct 23 2014 Karsten Hopp <karsten@redhat.com> 7.4.488-1
- patchlevel 488

* Wed Oct 22 2014 Karsten Hopp <karsten@redhat.com> 7.4.487-1
- patchlevel 487

* Tue Oct 21 2014 Karsten Hopp <karsten@redhat.com> 7.4.483-1
- patchlevel 483

* Fri Oct 17 2014 Karsten Hopp <karsten@redhat.com> 7.4.481-1
- patchlevel 481

* Thu Oct 16 2014 Karsten Hopp <karsten@redhat.com> 7.4.480-1
- patchlevel 480

* Wed Oct 15 2014 Karsten Hopp <karsten@redhat.com> 7.4.477-1
- patchlevel 477

* Mon Oct 13 2014 Karsten Hopp <karsten@redhat.com> 7.4.475-2
- add support for %%license macro (Petr Šabata)

* Sat Oct 11 2014 Karsten Hopp <karsten@redhat.com> 7.4.475-1
- patchlevel 475

* Fri Oct 10 2014 Karsten Hopp <karsten@redhat.com> 7.4.473-1
- patchlevel 473

* Thu Oct 09 2014 Karsten Hopp <karsten@redhat.com> 7.4.471-1
- patchlevel 471

* Tue Oct 07 2014 Karsten Hopp <karsten@redhat.com> 7.4.465-1
- patchlevel 465

* Tue Sep 30 2014 Karsten Hopp <karsten@redhat.com> 7.4.463-1
- patchlevel 463

* Mon Sep 29 2014 Karsten Hopp <karsten@redhat.com> 7.4.462-1
- patchlevel 462

* Sat Sep 27 2014 Karsten Hopp <karsten@redhat.com> 7.4.461-1
- patchlevel 461

* Wed Sep 24 2014 Karsten Hopp <karsten@redhat.com> 7.4.460-1
- patchlevel 460

* Wed Sep 24 2014 Karsten Hopp <karsten@redhat.com> 7.4.458-1
- patchlevel 458

* Tue Sep 23 2014 Karsten Hopp <karsten@redhat.com> 7.4.457-1
- patchlevel 457

* Sat Sep 20 2014 Karsten Hopp <karsten@redhat.com> 7.4.453-1
- patchlevel 453

* Tue Sep 16 2014 Karsten Hopp <karsten@redhat.com> 7.4.444-1
- patchlevel 444

* Mon Sep 15 2014 Karsten Hopp <karsten@redhat.com> 7.4.443-1
- patchlevel 443

* Wed Sep 10 2014 Karsten Hopp <karsten@redhat.com> 7.4.442-1
- patchlevel 442

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.4.417-2
- Perl 5.20 rebuild

* Tue Aug 26 2014 Karsten Hopp <karsten@redhat.com> 7.4.417-1
- patchlevel 417

* Fri Aug 22 2014 Karsten Hopp <karsten@redhat.com> 7.4.410-1
- patchlevel 410
- xsubpp-path patch is obsolete now

* Fri Aug 22 2014 Karsten Hopp <karsten@redhat.com> 7.4.402-3
- fix help file names

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.4.402-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild


* Wed Aug 13 2014 Karsten Hopp <karsten@redhat.com> 7.4.402-1
- patchlevel 402

* Tue Aug 12 2014 Karsten Hopp <karsten@redhat.com> 7.4.401-1
- patchlevel 401

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> 2:7.4.373-2
- fix license handling

* Tue Jul 22 2014 Karsten Hopp <karsten@redhat.com> 7.4.373-1
- patchlevel 373

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.4.307-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Karsten Hopp <karsten@redhat.com> 7.4.307-1
- patchlevel 307

* Tue Apr 29 2014 Vít Ondruch <vondruch@redhat.com> - 2:7.4.258-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Apr 16 2014 Karsten Hopp <karsten@redhat.com> 7.4.258-1
- patchlevel 258

* Mon Apr 07 2014 Karsten Hopp <karsten@redhat.com> 7.4.253-1
- patchlevel 253

* Wed Mar 12 2014 Karsten Hopp <karsten@redhat.com> 7.4.204-1
- patchlevel 204

* Mon Feb 24 2014 Karsten Hopp <karsten@redhat.com> 7.4.192-1
- patchlevel 192

* Tue Feb 18 2014 Karsten Hopp <karsten@redhat.com> 7.4.182-1
- patchlevel 182

* Tue Feb 18 2014 Karsten Hopp <karsten@redhat.com> 7.4.179-2
- enable dynamic lua interpreter

* Sat Feb 15 2014 Karsten Hopp <karsten@redhat.com> 7.4.179-1
- patchlevel 179

* Wed Jan 29 2014 Karsten Hopp <karsten@redhat.com> 7.4.160-1
- patchlevel 160

* Tue Dec 17 2013 Karsten Hopp <karsten@redhat.com> 7.4.131-1
- patchlevel 131

* Wed Nov 20 2013 Karsten Hopp <karsten@redhat.com> 7.4.094-1
- patchlevel 094

* Tue Oct 15 2013 Karsten Hopp <karsten@redhat.com> 7.4.052-1
- patchlevel 052

* Wed Sep 11 2013 Karsten Hopp <karsten@redhat.com> 7.4.027-2
- update vim icons (#1004788)
- check if 'id -u' returns empty string (vim.sh)

* Wed Sep 11 2013 Karsten Hopp <karsten@redhat.com> 7.4.027-1
- patchlevel 027

* Wed Sep 04 2013 Karsten Hopp <karsten@redhat.com> 7.4.016-1
- patchlevel 016

* Wed Aug 28 2013 Karsten Hopp <karsten@redhat.com> 7.4.009-1
- patchlevel 009
  mkdir("foo/bar/", "p") gives an error message
  creating a preview window on startup messes up the screen
  new regexp engine can't be interrupted
  too easy to write a file was not decrypted (yet)

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.5-1
- patchlevel 5
- when closing a window fails ":bwipe" may hang
- "vaB" while 'virtualedit' is set selects the wrong area

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.3-1
- patchlevel 3, memory access error in Ruby syntax highlighting

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.2-1
- patchlevel 2, pattern with two alternative look-behind matches doesn't match

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.1-1
- patchlevel 1, 'ic' doesn't work for patterns such as [a-z]

* Mon Aug 12 2013 Karsten Hopp <karsten@redhat.com> 7.4.0-1
- update to vim-7.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.3.1314-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Karsten Hopp <karsten@redhat.com> 7.3.1314-2
- document gex and vimx in man page
- fix gvimdiff and gvimtutor man page redirects

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2:7.3.1314-2
- Perl 5.18 rebuild

* Tue Jul 09 2013 Karsten Hopp <karsten@redhat.com> 7.3.1314-1
- patchlevel 1314

* Thu Jul 04 2013 Karsten Hopp <karsten@redhat.com> 7.3.1293-1
- patchlevel 1293

* Fri Jun 14 2013 Karsten Hopp <karsten@redhat.com> 7.3.1189-1
- patchlevel 1189

* Tue Jun 04 2013 Karsten Hopp <karsten@redhat.com> 7.3.1109-1
- patchlevel 1109

* Wed May 22 2013 Karsten Hopp <karsten@redhat.com> 7.3.1004-1
- patchlevel 1004

* Wed May 22 2013 Karsten Hopp <karsten@redhat.com> 7.3.1000-1
- patchlevel 1000 !

* Tue May 21 2013 Karsten Hopp <karsten@redhat.com> 7.3.987-1
- patchlevel 987

* Tue May 21 2013 Karsten Hopp <karsten@redhat.com> 7.3.944-2
- consistent use of macros in spec file
- add some links to man pages

* Tue May 14 2013 Karsten Hopp <karsten@redhat.com> 7.3.944-1
- patchlevel 944

* Mon May 13 2013 Karsten Hopp <karsten@redhat.com> 7.3.943-2
- add BR perl(ExtUtils::ParseXS)

* Mon May 13 2013 Karsten Hopp <karsten@redhat.com> 7.3.943-1
- patchlevel 943

* Wed May 08 2013 Karsten Hopp <karsten@redhat.com> 7.3.931-1
- patchlevel 931

* Wed May 08 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- fix ruby version check

* Fri Apr 19 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- drop crv patch
- update 7.3.838 patch, it was broken upstream

* Mon Apr 15 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- patchlevel 903

* Mon Feb 18 2013 Karsten Hopp <karsten@redhat.com> 7.3.822-1
- patchlevel 822

* Fri Feb 15 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 7.3.797-2
- Only use --vendor for desktop-file-install on F18 or less

* Thu Jan 31 2013 Karsten Hopp <karsten@redhat.com> 7.3.797-1
- patchlevel 797

* Mon Jan 28 2013 Karsten Hopp <karsten@redhat.com> 7.3.785-1
- patchlevel 785

* Tue Nov 20 2012 Karsten Hopp <karsten@redhat.com> 7.3.715-1
- patchlevel 715

* Mon Nov 12 2012 Karsten Hopp <karsten@redhat.com> 7.3.712-1
- patchlevel 712

* Mon Nov 12 2012 Karsten Hopp <karsten@redhat.com> 7.3.682-2
- fix vim.csh syntax

* Tue Oct 23 2012 Karsten Hopp <karsten@redhat.com> 7.3.712-1
- patchlevel 712

* Mon Oct 15 2012 Karsten Hopp <karsten@redhat.com> 7.3.691-1
- patchlevel 691

* Fri Oct 05 2012 Karsten Hopp <karsten@redhat.com> 7.3.682-1
- patchlevel 682
- use --enable-rubyinterp=dynamic and --enable-pythoninterp=dynamic

* Mon Sep 03 2012 Karsten Hopp <karsten@redhat.com> 7.3.646-1
- patchlevel 646

* Tue Aug 28 2012 Karsten Hopp <karsten@redhat.com> 7.3.638-2
- fix some man page typos (#668894, #675480)
- own usr/share/vim/vimfiles/doc/tags (#845564)
- add path to csope database (#844843)

* Tue Aug 28 2012 Karsten Hopp <karsten@redhat.com> 7.3.638-1
- patchlevel 638

# vim:nrformats-=octal
