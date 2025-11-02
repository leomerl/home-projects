import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# Defining 2 tensotrs
X = torch.tensor([[0.0], [1.0], [2.0], [3.0]])
y = torch.tensor([[3.0], [5.0], [7.0], [9.0]])

# Defining a linear layer
linear_layer = nn.Linear(in_features=1, out_features=1)

print("Initial weight:", linear_layer.weight)
print("Initial bias:", linear_layer.bias)

# Loss function: Mean Squared Error
loss_function = nn.MSELoss()

# Defining an optimizer: Stochastic Gradient Descent
optimizer = optim.SGD(params=linear_layer.parameters(), lr=0.01) # lr=0.01 is the learning rate.

#  Training loop
for epoch in range(1100):
    y_pred = linear_layer(X)
    loss = loss_function(y_pred, y)
    
    optimizer.zero_grad()
    loss.backward() # computes derivatives of loss w.r.t. weight and bias.
    optimizer.step() # Update weights and bias
    
    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}, w: {linear_layer.weight.item():.4f}, b: {linear_layer.bias.item():.4f}")


## plotting
plt.scatter(X.numpy(), y.numpy(), color='blue', label='Original Data')

with torch.no_grad():
    y_pred = linear_layer(X)

plt.plot(X.numpy(), y_pred.numpy(), color='red', label='Fitted Line')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show() # 2x + 3