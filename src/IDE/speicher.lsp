(define tmp_window (toplevel$ "tmp"))
(define txt (text$ tmp_window))
(txt 'pack)
(define btn_save (button$ btn_panel "save" (lambda (x) (txt 'setText (tf_input 'getText)))))
(btn_save 'pack)