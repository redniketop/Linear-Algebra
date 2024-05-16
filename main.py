from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from sympy import Matrix

# Create an instance of FastAPI
app = FastAPI()

# Define the data model for the matrix input using Pydantic
class MatrixData(BaseModel):
    data: list[list[float]]  # A list of lists of floats representing the matrix

    # Validator to ensure the matrix is square
    @field_validator('data')
    def must_be_square(cls, v):
        # Check if the matrix is empty or if any row length is not equal to the number of rows
        if len(v) == 0 or any(len(row) != len(v) for row in v):
            raise ValueError("Must be a square matrix")  # Raise an error if not square
        return v  # Return the value if it is a square matrix

# Define a POST endpoint for row reduction
@app.post("/row-reduction/")
async def calculate_row_reduction(matrix: MatrixData):
    try:
        # Convert the input matrix to a SymPy matrix
        sympy_matrix = Matrix(matrix.data)
        # Perform row reduction to reduced row echelon form (RREF)
        rref_matrix, pivot_cols = sympy_matrix.rref()
        # Convert the RREF matrix to a list of lists of floats
        rref_list = [[float(num) for num in row] for row in rref_matrix.tolist()]

        # Convert the pivot columns to a list of integers
        pivot_cols_list = [int(col) for col in pivot_cols]

        # Debug output to trace issues
        print(f"Received matrix: {matrix.data}")
        print(f"RREF Matrix: {rref_list}")
        print(f"Pivot Columns: {pivot_cols_list}")

        # Prepare the response data
        response_data = {
            "rref": rref_list,
            "pivot_columns": pivot_cols_list
        }

        # Debug output to trace issues
        print(f"Response data: {response_data}")

        # Return the response data
        return response_data
    except Exception as e:
        # Log the error and raise an HTTPException with a 400 status code
        print(f"Error in /row-reduction/: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Define a POST endpoint for calculating the determinant
@app.post("/determinant/")
async def calculate_determinant(matrix: MatrixData):
    try:
        # Convert the input matrix to a SymPy matrix
        sympy_matrix = Matrix(matrix.data)
        # Calculate the determinant of the matrix
        determinant = sympy_matrix.det()

        # Debug output to trace issues
        print(f"Received matrix: {matrix.data}")
        print(f"Determinant: {determinant}")

        # Return the determinant as a float
        return {"determinant": float(determinant)}
    except Exception as e:
        # Log the error and raise an HTTPException with a 400 status code
        print(f"Error in /determinant/: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Run the FastAPI application using Uvicorn if this script is run directly
if __name__ == "__main__":
    import uvicorn
    # Run the application on localhost (127.0.0.1) at port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
