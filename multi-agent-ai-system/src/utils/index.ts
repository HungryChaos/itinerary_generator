export function generateRandomNumber(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function calculateReward(success: boolean): number {
    return success ? 1 : -1;
}