export const validatePayload = (payload) => {
  if(payload == null) {
    return {
      nonFieldError: "Error: could not establish a connection to the server."
    }
  } else if(payload && payload.errors) {
    return payload.errors;
  }
  return null;
};
