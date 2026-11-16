# L1 vs. L2 Regularization — Voiceover Script

The cues below follow the rendered video. Pause or hold on a visual whenever you need more time to speak.

## Opening: title, network, and the two sums

**[Title appears]**

What’s the difference between L1 and L2 regularization, beyond using the sum of absolute weights versus the sum of squared weights?

**[Neural network appears; the weights gather into the two formulas]**

Both methods add a penalty based on the model’s weights. But they affect small weights in different ways.

## L1 can reach zero

**[L1 moves to the center; some red weights shrink to zero]**

L1 regularization can push some weights all the way to zero, especially when the corresponding features aren’t useful.

## L2 shrinks weights

**[L2 replaces L1; the red weights become small again]**

L2 regularization also pulls weights toward zero. But it usually makes them smaller without setting them exactly to zero.

## The question

**[Theta appears and asks why]**

So why does that happen? Let’s look at the math.

## L2: cost function and derivative

**[L2 cost function appears]**

For L2 regularization, we add the sum of the squared weights to the loss, scaled by lambda over two m.

**[Derivative appears]**

Now take the derivative with respect to one weight, w. The derivative of the L2 penalty contributes lambda over m times w.

## L2: update rule and rearranging

**[Gradient descent update appears]**

So the gradient descent update subtracts both the loss gradient and this regularization term.

**[The equation rearranges]**

Rearranging the terms, we can factor out w. It gets multiplied by one minus alpha lambda over m, while the usual loss-gradient update is still applied.

## L2: weight decay

**[The factor is highlighted; the bar shrinks]**

When alpha lambda over m is small, that multiplier is just a little less than one. At every step, the current weight is scaled down by a fraction. This is why L2 is often associated with weight decay.

Notice what happens to the bar. Each step removes a fraction of what remains, so the amount removed gets smaller as the weight shrinks. Even after many steps, zooming in reveals a tiny positive value: the decay approaches zero without forcing the weight to become exactly zero.

## L1: cost function and derivative

**[The screen switches to the L1 equations]**

Now L1 adds the sum of the absolute values of the weights, scaled by lambda over m.

For any nonzero weight, the derivative of its absolute value is its sign: positive one for a positive weight, and negative one for a negative weight. At zero, the absolute value isn’t differentiable, so we use a subgradient.

## L1: update rule and constant pull

**[The update rule appears; the regularization term is highlighted]**

The update now includes a pull toward zero whose magnitude is constant for every nonzero weight. If that pull is zero point one, it removes the same amount from a positive weight at each step.

**[The bar loses equal-sized pieces until it reaches zero]**

As the bar gets smaller, the amount removed stays the same. If the loss doesn’t need that weight enough to counter the penalty, the weight can reach exactly zero. The model is then sparse: some weights contribute nothing.

So the key difference is the kind of pull. L2 shrinks weights by a fraction; L1 can remove a fixed amount and set some weights to zero.
