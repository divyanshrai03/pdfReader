from temp import Model

obj  = Model(question="what is my name", context="my name is vivek, i am in vit chennai")

output = obj.getResponse()
print(output.text)


response = self.model.generate_content(f"you are a smart ai who has to answer the question :{self.qes} using the following context: {self.context} only, if there is no relavent information in the context just reply with text as i do not have any specific information on that, if there is relavent information in context based on quetion, reply in the most simple and on point way")