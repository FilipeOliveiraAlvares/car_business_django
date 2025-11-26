from django import forms
from carros.models import Carro, ModeloVeiculo, VersaoVeiculo, CategoriaVeiculo, Marca


class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = [
            # "categoria",  # Temporariamente oculto - será reativado quando houver motos, caminhões, etc.
            "marca",
            "modelo",
            "versao",
            "nome",
            "ano",
            "preco",
            "combustivel",
            "cambio",
            "portas",
            "km",
            "cor",
            "descricao",
            "foto_principal",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Categorias e marcas ordenadas
        # self.fields["categoria"].queryset = CategoriaVeiculo.objects.all().order_by("nome")  # Temporariamente desabilitado
        self.fields["marca"].queryset = Marca.objects.all().order_by("nome")

        # ------------------------------
        #   MODELOS
        # ------------------------------
        marca_valor = self.data.get("marca") or self.data.get("id_marca")

        if marca_valor:
            try:
                marca_id = int(marca_valor)
                self.fields["modelo"].queryset = ModeloVeiculo.objects.filter(
                    marca_id=marca_id
                ).order_by("nome")
            except (ValueError, TypeError):
                self.fields["modelo"].queryset = ModeloVeiculo.objects.none()

        elif self.instance.pk and self.instance.marca:
            self.fields["modelo"].queryset = ModeloVeiculo.objects.filter(
                marca=self.instance.marca
            ).order_by("nome")

        else:
            self.fields["modelo"].queryset = ModeloVeiculo.objects.none()

        # ------------------------------
        #   VERSÕES
        # ------------------------------
        modelo_valor = self.data.get("modelo") or self.data.get("id_modelo")

        if modelo_valor:
            try:
                modelo_id = int(modelo_valor)
                self.fields["versao"].queryset = VersaoVeiculo.objects.filter(
                    modelo_id=modelo_id
                ).order_by("nome")
            except (ValueError, TypeError):
                self.fields["versao"].queryset = VersaoVeiculo.objects.none()

        elif self.instance.pk and self.instance.modelo:
            self.fields["versao"].queryset = VersaoVeiculo.objects.filter(
                modelo=self.instance.modelo
            ).order_by("nome")

        else:
            self.fields["versao"].queryset = VersaoVeiculo.objects.none()

        # Foto principal é sempre obrigatória (criação e edição)
        if not self.instance.pk:
            # Ao criar: campo obrigatório
            self.fields["foto_principal"].required = True
            self.fields["foto_principal"].help_text = "Foto principal é obrigatória para criar um veículo."
        else:
            # Ao editar: não é required no campo (pode manter a existente), mas validamos no clean
            self.fields["foto_principal"].required = False
            self.fields["foto_principal"].help_text = "Se não selecionar uma nova foto, a foto atual será mantida. A foto principal é obrigatória."
    
    def clean_foto_principal(self):
        foto_principal = self.cleaned_data.get('foto_principal')
        instance = self.instance
        
        # Se está editando
        if instance and instance.pk:
            # Se não enviou nova foto, mantém a existente
            if not foto_principal:
                # Retorna a foto existente para não perder
                return instance.foto_principal
            # Se enviou nova foto, valida e usa a nova
            return foto_principal
        
        # Se está criando, foto é obrigatória (já validado no required)
        if not foto_principal:
            raise forms.ValidationError(
                "A foto principal é obrigatória para criar um veículo."
            )
        
        return foto_principal
