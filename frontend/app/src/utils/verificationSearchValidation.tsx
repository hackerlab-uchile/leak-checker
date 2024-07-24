type ValidationResponse = { valid: boolean; reason: string };

export function validateMobileNumber(v: string): ValidationResponse {
  let phoneRegex = /^[\d]{8}$/;
  if (phoneRegex.test(v)) return { valid: true, reason: "" };
  else
    return {
      valid: false,
      reason: "Formato de número celular inválido. Ejemplo: 87654321",
    };
}
