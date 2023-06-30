from services.code_generation_service import CodeGenerationService


template = "$Hello $ONE$ hi $ADFJKL$ there $THREE$ three"
cgs = CodeGenerationService(template, None, None, True)
print(cgs.generateCode())