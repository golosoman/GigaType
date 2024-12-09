// export const ZoneToNameZone = {
//   "Зона 1 (ФЫВАОЛДЖ)": "фываолдж",
//   "Зона 2 (ПР)": "пр",
//   "Зона 3 (КЕНГ)": "кенг",
//   "Зона 4 (МИТЬ)": "мить",
//   "Зона 5 (УСШБ)": "усшб",
//   "Зона 6 (ЦЧЩЮ)": "цчщю",
//   "Зона 7 (ЁЙЯЗХЪЭ.,)": "ёйязхъэ.,",
//   "Зона 8 (1234567890)": "1234567890",
//   "Зона 9 (символы)": '!"№;%:?*()_-+=',
//   "Зона Пробела": " ",
// };

type Zone = { keys: string; uid: string };
type ZoneKey = string; // Здесь можно уточнить тип, если у вас есть фиксированный набор ключей

export const getUidsFromSelectedOptions = (
  selectedOptions: ZoneKey[],
  extractedZones: Zone[],
  zoneToNameZone: Record<ZoneKey, string>
): string[] => {
  const keys = selectedOptions
    .map((option) => zoneToNameZone[option])
    .filter((key) => key !== undefined);

  const uids = extractedZones
    .filter((zone) => keys.includes(zone.keys))
    .map((zone) => zone.uid);

  return uids;
};

export const NameZoneToZone = {
  фываолдж: "Зона 1 (ФЫВАОЛДЖ)",
  пр: "Зона 2 (ПР)",
  кенг: "Зона 3 (КЕНГ)",
  мить: "Зона 4 (МИТЬ)",
  усшб: "Зона 5 (УСШБ)",
  цчщю: "Зона 6 (ЦЧЩЮ)",
  "ёйязхъэ.,": "Зона 7 (ЁЙЯЗХЪЭ.,)",
  "1234567890": "Зона 8 (1234567890)",
  '!"№;%:?*()_-+=': "Зона 9 (символы)",
  " ": "Зона Пробела",
};
// Теперь вы можете использовать keyof для получения типа ключей
type NameZoneKeys = keyof typeof NameZoneToZone;

// Метод преобразования зон
export const transformZones = (zones: { keys: string; uid: string }[]) => {
  return zones.map((zone) => {
    // Приведение к верхнему регистру
    const upperKeys = zone.keys.toUpperCase();

    // Ищем название зоны по ключу в инвертированном объекте
    const foundZone = NameZoneToZone[zone.keys as NameZoneKeys];

    return foundZone ? foundZone : upperKeys;
  });
};
