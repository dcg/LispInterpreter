(define tf_input +)
(define tf_output +)

(define eval_input (lambda (x) (tf_output 'setText (eval (tf_input 'getText)))))
(define load_file (lambda (x) (tf_input 'setText (load "IDE/moreGui.lsp"))))



 
(define get_wrap_eval_code (lambda (x) (tf_input 'setText get_wrap_eval_code_str)))
(begin
        (define root (tk$))
        (define w (label$ root "self building lisp gui"))
        (w 'pack)
        (define p_input (frame$ root))
        (set! tf_input (text$ p_input))
        (tf_input 'pack)
        (p_input 'pack)
        (define btn_panel (frame$ root))
        (btn_panel 'pack)
        (define b_eval (button$ btn_panel "Eval" eval_input))
        (b_eval 'pack)

        
        (define b_test (button$ btn_panel "Load greater GUI" load_file))
        (b_test 'pack)
        (set! tf_output (text$ root))
        (tf_output 'pack)
         )
(root 'mainloop)