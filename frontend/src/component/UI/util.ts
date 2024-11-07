export const setUniqId = () => {
  const date = new Date();
  const timestamp = date.getTime();
  const randomString = Math.random().toString(36).substring(7);
  const randomNumber = Math.floor(Math.random() * 10000);
  const uniqueId = `id-${timestamp}-${randomString}-${randomNumber}`;
  return uniqueId;
};
