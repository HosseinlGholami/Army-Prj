FROM rabbitmq:3-management

COPY ./Conf/definitions.json /etc/rabbitmq/
COPY ./Conf/enabled_plugins /etc/rabbitmq/
COPY ./Conf/rabbitmq.conf /etc/rabbitmq/

#RUN rabbitmq-plugins enable rabbitmq_shovel 
#RUN rabbitmq-plugins enable rabbitmq_shovel_management

RUN rabbitmq-plugins enable rabbitmq_federation
RUN rabbitmq-plugins enable rabbitmq_federation_management

EXPOSE 5672
EXPOSE 15672
