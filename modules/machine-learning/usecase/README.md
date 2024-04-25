# Usecases

This module hosts the application layer code that contains
the business usecase logic, and is client of the domain layer
it uses the domain layer coarse-grainted functionality to finish
it logic.

Application layer wraps the logic for each usecase in a corresponding
function that has name literally indicating the purporse of its represented usecase.

Bussiness usecase abstracts the domain layer logic by a coarse-grained API (functions
that represent the usecase), and it prevent domain layer from adulterated by infrastructure complexity

it contains logic that the domain layer should not contain, for example the logic of checking the number of 
current jobs running, then compare this number to the max number of jobs running that allow (to prevent our 
instance not to be overloaded, stagnant), this kind of logic is related to infrastructure, availability concern.
