function manage_participacao(){
  if ($('#id_participacao option:selected').val() == 'AC' || $('#id_participacao option:selected').val() == 'AP') {
    $('#pub').css('display', 'block');
  }
  else {
    $('#pub').css('display', 'none');
   
  }
}

function manage_vinculo(){
  if ($('#id_vinculo option:selected').val() == 'OU') {
    $('#outro_1').css('display', 'block');
  }
  else {
    $('#outro_1').css('display', 'none');
  }
}

function manage_titulacao(){
  if ($('#id_titulacao option:selected').val() == 'OU') {
    $('#outro_2').css('display', 'block');
  }
  else {
    $('#outro_2').css('display', 'none');
  }
}


function validaCamposA()
	{
		document.form.situacao.value = 'Aprovado';
		document.form.submit();
	}

function validaCamposN()
	{
    	document.form.situacao.value = 'Reprovado';
		document.form.submit();
	}



$(function() {
  $("#id_participacao").change(manage_participacao);
  $("#id_titulacao").change(manage_titulacao);
  $("#id_vinculo").change(manage_vinculo);
});

jQuery(function($){
   $("#id_telefone").mask("(99) 9999-9999");
   $("#id_celular").mask("(99) 9999-9999");
   $("#id_cpf").mask("999.999.999-99");
});
