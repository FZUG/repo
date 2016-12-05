(add-to-list 'load-path "/usr/share/emacs/site-lisp/mozc")
(setq mozc-helper-program-name "/usr/bin/mozc_emacs_helper")

(require 'mozc)
;; To make this input method default -
; (set-language-environment "Japanese")
; (setq default-input-method "japanese-mozc")
