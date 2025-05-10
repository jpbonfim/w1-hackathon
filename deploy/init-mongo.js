
user_dummy = {
    user_id: "fc9dfa83-4a94-4090-a8ce-3110799bf690",
    name: "Rodrigo Lima",
    nickname: "Rodrigo",
    email: "rodrigo.lima@gmail.com",
    cpf: "40712345600",
}

db = db.getSiblingDB("hackathon-w1");
db.createCollection("users");
db.users.insertOne(user_dummy);
