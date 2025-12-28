export const safeArray = <T>(v?: T[] | null): T[] => (Array.isArray(v) ? v : []);

export const safeNum = (v: any): number | null => {
  return Number.isFinite(v) ? v : null;
};

export const formatNaira = (v: any, placeholder = 'N/A'): string => {
  const n = safeNum(v);
  return n !== null ? `₦${n.toLocaleString()}` : placeholder;
};

export const safeString = (s: any, def = ''): string => (s ?? def).toString();

export const includesSafe = (s: any, sub: string): boolean => {
  try {
    return (s ?? '').toString().includes(sub);
  } catch {
    return false;
  }
};

export const safeFixed = (v: any, digits = 2, placeholder = 'N/A') => {
  const n = safeNum(v);
  return n !== null ? n.toFixed(digits) : placeholder;
};
