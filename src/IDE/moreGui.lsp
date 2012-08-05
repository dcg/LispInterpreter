(begin
(define t_bytecode (lambda x (+ x 666666666666666)))
(define t_optcode (lambda x (+ x 55555555555555)))
(define eval_input2
 	(lambda (x) 
 		(tf_output 'setText (eval (str_concat "(begin " (tf_input 'getText) ")")))
 	)
 )
 
 (define (wrap_input_in_begin x) (str_concat "(begin " x ")")	)
 
 
 (define (eval_show_bc x) (begin 
  		(define result (eval (wrap_input_in_begin (tf_input 'getText))))
  		(if (eq? (type result) "UserFunction") (t_bytecode 'setText (call result '++bc++)) (t_bytecode 'setText "NO BYTECODE!!!"))
  		(if (eq? (type result) "UserFunction") (t_optcode 'setText (call result '++op++)) (t_optcode 'setText "NO OPTCODE!!!"))
  		(tf_output 'setText result)
  		)
  )
 
 
 (define b_eval_begin (button$ btn_panel "Eval-with-Begin" eval_show_bc))
 (b_eval_begin 'pack)
 
 (define b_clear (button$ btn_panel "clear" (lambda (x) (tf_input 'setText ""))))
 (b_clear 'pack)
 (define sb_input (scrollbar$ p_input))
 (sb_input 'pack)
 (tf_input 'setScrollbar sb_input)
 (sb_input 'setParent tf_input)
 (tf_input 'setBG "BLACK")
 (tf_input 'setCursorColor "GREEN")
 (tf_input 'setFG "WHITE")
 (tf_output 'setBG "PINK")
 (tf_output 'setFG "BLACK")
 (b_eval_begin 'setBG "GREEN")
 (b_eval 'setBG "BLACK")
 (b_eval 'setFG "WHITE")
 
 (define tl_bc (toplevel$ "Bytecode"))
 (define l_bytecode (label$ tl_bc "Bytecode"))
 (l_bytecode 'pack)
 (set! t_bytecode (text$ tl_bc))
 (t_bytecode 'pack)
 (define tl_optcode (toplevel$ "Opt-Code"))
  (define l_optcode (label$ tl_optcode "Opt-Code"))
 (l_optcode 'pack)
  (set! t_optcode (text$ tl_optcode))
 (t_optcode 'pack)
 
 
 )