from transformers import BertForSequenceClassification
import torch.nn as nn

class MyModel1(BertForSequenceClassification):
    def __init__(self, config):
        super(MyModel1, self).__init__(config)
        # 필요한 경우 여기에 추가 레이어나 변경 사항을 추가할 수 있습니다.
        # 예: self.new_layer = nn.Linear(config.hidden_size, custom_size)

    def forward(self, input_ids, attention_mask=None, token_type_ids=None, position_ids=None, head_mask=None, inputs_embeds=None, labels=None):
        # BERT 모델의 forward 메서드를 호출합니다.
        # 필요한 경우 이 부분을 수정하여 커스텀 동작을 추가할 수 있습니다.
        return super(MyModel1, self).forward(
            input_ids, 
            attention_mask=attention_mask, 
            token_type_ids=token_type_ids, 
            position_ids=position_ids, 
            head_mask=head_mask, 
            inputs_embeds=inputs_embeds, 
            labels=labels
        )

# 모델을 인스턴스화하고 사전 훈련된 가중치를 로드하는 코드는 다음과 같습니다.
# model = MyModel1.from_pretrained('bert-base-uncased', num_labels=number_of_labels)
# 이 부분은 실제 코드에서 필요에 따라 사용하시면 됩니다.
